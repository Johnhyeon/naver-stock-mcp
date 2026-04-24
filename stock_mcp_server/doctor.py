"""StockLens 설치·설정 진단 도구.

실행: `stocklens-doctor` 또는 `python -m stock_mcp_server.doctor`

체크 항목:
- uv 설치 여부 (Python 런타임 관리자)
- stocklens-mcp 패키지 import 가능 여부
- stocklens 실행 명령 탐색 (PATH / uv tool bin / sysconfig)
- Claude Desktop config 파일
- config 내 stocklens entry 유효성 (command resolvable)
- Legacy 키 잔존 여부
"""

import json
import os
import shutil
import sys
import sysconfig
from pathlib import Path


# setup_claude와 일관성 유지
try:
    from stock_mcp_server.setup_claude import (
        get_config_path,
        SERVER_KEY,
        LEGACY_KEYS,
        _uv_tool_bin_dirs,
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from stock_mcp_server.setup_claude import (
        get_config_path,
        SERVER_KEY,
        LEGACY_KEYS,
        _uv_tool_bin_dirs,
    )


class Check:
    def __init__(self, name: str):
        self.name = name
        self.status = None  # "ok" / "warn" / "fail"
        self.lines: list[str] = []
        self.fix: str | None = None

    def ok(self, msg: str):
        self.status = "ok"
        self.lines.append(msg)
        return self

    def warn(self, msg: str, fix: str | None = None):
        if self.status != "fail":
            self.status = "warn"
        self.lines.append(msg)
        if fix:
            self.fix = fix
        return self

    def fail(self, msg: str, fix: str | None = None):
        self.status = "fail"
        self.lines.append(msg)
        if fix:
            self.fix = fix
        return self

    def info(self, msg: str):
        self.lines.append(msg)
        return self


def check_uv() -> Check:
    c = Check("uv (Python runtime manager)")
    uv = shutil.which("uv")
    if uv:
        c.ok("uv is installed")
        c.info(f"Path:       {uv}")
    else:
        # uv 없이도 stocklens가 동작 가능 (pip 설치 등)이지만,
        # 권장 설치 경로는 uv이므로 warn으로 안내.
        c.warn(
            "uv not found in PATH",
            fix=(
                "Install uv (recommended):\n"
                "  Windows: irm https://astral.sh/uv/install.ps1 | iex\n"
                "  macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh"
            ),
        )
    return c


def check_package() -> Check:
    c = Check("Package (stocklens-mcp)")
    try:
        import stock_mcp_server  # noqa: F401
        c.ok("stocklens-mcp is importable")
        c.info(f"Location:   {Path(stock_mcp_server.__file__).parent}")
        c.info(f"Python:     {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        c.info(f"Executable: {sys.executable}")
    except ImportError:
        c.fail(
            "stocklens-mcp NOT importable in current interpreter",
            fix="uv tool install --force stocklens-mcp",
        )
    return c


def check_stocklens_command() -> Check:
    c = Check("Command (stocklens)")
    # 1) PATH 탐색
    exe = shutil.which("stocklens")
    if exe:
        c.ok("'stocklens' found in PATH")
        c.info(f"Path:       {exe}")
        return c

    # 2) uv tool bin 디렉토리 직접 확인
    for bin_dir in _uv_tool_bin_dirs():
        for name in ("stocklens.exe", "stocklens"):
            candidate = bin_dir / name
            if candidate.exists():
                c.warn(
                    "'stocklens' exists but not on PATH",
                    fix=(
                        f'Add to PATH: "{bin_dir}"\n'
                        f'(or proceed — setup_claude will use absolute path)'
                    ),
                )
                c.info(f"Path:       {candidate}")
                return c

    # 3) sysconfig scripts 디렉토리 (pip 설치 호환)
    try:
        scripts_dir = Path(sysconfig.get_paths()["scripts"])
        for name in ("stocklens.exe", "stocklens"):
            candidate = scripts_dir / name
            if candidate.exists():
                c.warn(
                    "'stocklens' exists in sysconfig scripts but not on PATH",
                    fix=f'Add to PATH: "{scripts_dir}"',
                )
                c.info(f"Path:       {candidate}")
                return c
    except Exception:
        pass

    # 4) 어디에도 없음
    c.fail(
        "'stocklens' command NOT found anywhere",
        fix="uv tool install --force stocklens-mcp",
    )
    return c


def check_config() -> Check:
    c = Check("Claude Desktop Config")
    config_path = get_config_path()

    # Store 버전 감지 알림
    if "Packages" in str(config_path) and "LocalCache" in str(config_path):
        c.info("Detected: Microsoft Store version (sandboxed path)")
    c.info(f"Path:       {config_path}")

    # 두 경로 모두 존재하는 비정상 케이스 경고
    from stock_mcp_server.setup_claude import _find_store_config_path
    store = _find_store_config_path()
    std_appdata = os.environ.get("APPDATA")
    std_path = Path(std_appdata) / "Claude" / "claude_desktop_config.json" if std_appdata else None
    if store and std_path and store.exists() and std_path.exists() and store != std_path:
        c.warn(
            f"Both Store and standard config files exist. Active: {config_path}",
            fix=f"Remove unused: {std_path if config_path == store else store}",
        )

    if not config_path.exists():
        c.fail(
            "Config file does not exist",
            fix="stocklens-setup",
        )
        return c

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except json.JSONDecodeError as e:
        c.fail(
            f"Config is not valid JSON: {e}",
            fix="Back up and re-run stocklens-setup",
        )
        return c
    except Exception as e:
        c.fail(f"Cannot read config: {e}")
        return c

    servers = cfg.get("mcpServers", {}) or {}
    entry = servers.get(SERVER_KEY)

    legacy_found = [k for k in LEGACY_KEYS if k in servers]
    if legacy_found:
        c.warn(
            f"Legacy entries present: {legacy_found}",
            fix="stocklens-setup (auto-removes)",
        )

    if not entry:
        c.fail(
            "'stocklens' entry missing in mcpServers",
            fix="stocklens-setup",
        )
        return c

    cmd = entry.get("command")
    args = entry.get("args", [])
    c.info(f"Command:    {cmd}")
    if args:
        c.info(f"Args:       {args}")

    if not cmd:
        c.fail("Entry has no 'command' field")
        return c

    if Path(cmd).is_absolute():
        if Path(cmd).exists():
            c.ok("Command points to existing file")
        else:
            c.fail(
                f"Command file missing: {cmd}",
                fix="stocklens-setup",
            )
    else:
        resolved = shutil.which(cmd)
        if resolved:
            c.ok(f"Command resolvable via PATH: {resolved}")
        else:
            c.fail(
                f"Command '{cmd}' not in PATH — Claude Desktop will fail to launch",
                fix="stocklens-setup",
            )

    return c


STATUS_ICON = {"ok": "[ OK ]", "warn": "[WARN]", "fail": "[FAIL]", None: "[ ?  ]"}


def print_check(c: Check):
    icon = STATUS_ICON.get(c.status, "[ ?  ]")
    print(f"{icon} {c.name}")
    for line in c.lines:
        print(f"       {line}")
    if c.fix:
        print(f"       Fix: {c.fix}")
    print()


def main():
    # Windows cp949 터미널 호환을 위해 stdout UTF-8 시도
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    print("=" * 60)
    print("  StockLens Doctor - Installation Diagnosis")
    print("=" * 60)
    print()

    checks = [
        check_uv(),
        check_package(),
        check_stocklens_command(),
        check_config(),
    ]

    for c in checks:
        print_check(c)

    any_fail = any(c.status == "fail" for c in checks)
    any_warn = any(c.status == "warn" for c in checks)

    print("=" * 60)
    if any_fail:
        print("  [FAIL] One or more critical issues found.")
        print("  Apply the 'Fix:' commands above, then re-run stocklens-doctor.")
        sys.exit(1)
    elif any_warn:
        print("  [WARN] Installation works but some warnings exist.")
        print("  If MCP appears in Claude Desktop, you're fine.")
    else:
        print("  [ OK ] All checks passed!")
        print("  If MCP still doesn't appear, FULLY QUIT Claude Desktop")
        print("  (tray icon -> Quit) and restart.")
    print("=" * 60)


if __name__ == "__main__":
    main()
