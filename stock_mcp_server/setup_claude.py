"""Configure Claude Desktop to use the stock-data MCP server.

Run `stock-mcp-setup` after installing the package.
"""

import json
import os
import sys
from pathlib import Path


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


def configure(command: str = "stock-mcp-server") -> None:
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

    config["mcpServers"]["stock-data"] = {"command": command}

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"  [OK] Config updated")
    print(f"  Path: {config_path}")


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "stock-mcp-server"
    print("==============================================")
    print("  naver-stock-mcp - Claude Desktop Setup")
    print("==============================================")
    print()
    try:
        configure(command)
        print()
        print("Done! Please restart Claude Desktop.")
    except Exception as e:
        print(f"  [ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
