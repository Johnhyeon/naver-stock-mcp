"""Configure Claude Desktop to use the StockLens MCP server.

Run `stocklens-setup` after installing the package.
"""

import json
import os
import sys
from pathlib import Path


# MCP 서버 키: 'stocklens'
# v0.1.x 호환용: 'stock-data'가 있으면 자동으로 제거 (마이그레이션)
SERVER_KEY = "stocklens"
LEGACY_KEYS = ["stock-data"]


def get_config_path() -> Path:
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA environment variable not found.")
        return Path(appdata) / "Claude" / "claude_desktop_config.json"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"


def configure(command: str = "stocklens") -> None:
    config_path = get_config_path()
    config_dir = config_path.parent
    config_dir.mkdir(parents=True, exist_ok=True)

    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            backup_path = config_path.with_suffix(".json.backup")
            with open(backup_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"  [OK] Backup saved: {backup_path}")
        except json.JSONDecodeError:
            print("  [WARN] Existing config is corrupted. Creating new one.")
            config = {}
    else:
        config = {}

    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # 이전 키 자동 정리 (마이그레이션)
    removed_legacy = []
    for legacy in LEGACY_KEYS:
        if legacy in config["mcpServers"]:
            del config["mcpServers"][legacy]
            removed_legacy.append(legacy)
    if removed_legacy:
        print(f"  [OK] Removed legacy entries: {', '.join(removed_legacy)}")

    # 새 키 등록
    config["mcpServers"][SERVER_KEY] = {"command": command}

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"  [OK] Config updated (key: {SERVER_KEY})")
    print(f"  Path: {config_path}")


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "stocklens"
    print("==============================================")
    print("  StockLens - Claude Desktop Setup")
    print("==============================================")
    print()
    try:
        configure(command)
        print()
        print("Done! Please fully quit and restart Claude Desktop.")
    except Exception as e:
        print(f"  [ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
