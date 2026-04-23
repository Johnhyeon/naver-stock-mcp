# StockLens Installation Guide

[🇰🇷 한국어](../ko/INSTALL.md) | [TOOLS](TOOLS.md) | [USAGE](USAGE.md)

---

## One-line install (recommended)

[`uv`](https://docs.astral.sh/uv/) installs the Python runtime for you. No separate Python install needed.

### Windows (PowerShell)

Open PowerShell (Start menu → search "PowerShell") and paste:

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://raw.githubusercontent.com/Johnhyeon/stocklens-mcp/main/install.ps1 | iex"
```

### macOS / Linux (terminal)

```bash
curl -LsSf https://raw.githubusercontent.com/Johnhyeon/stocklens-mcp/main/install.sh | sh
```

### What the install script does

1. **Check / install uv** — runs the official [astral.sh](https://astral.sh/uv/) installer if missing (Python runtime included)
2. **Install stocklens-mcp** — `uv tool install` (isolated env, no system Python pollution)
3. **Register Claude Desktop config** — adds an absolute-path entry to `claude_desktop_config.json` (no PATH dependency)
4. **Verify** — runs `stocklens-doctor`, exits non-zero on critical issues

---

## Manual install (3 steps)

If you prefer not to pipe a script:

```bash
# 1) Install uv
# Windows
powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2) Install stocklens-mcp
uv tool install stocklens-mcp

# 3) Register Claude Desktop config
stocklens-setup
```

---

## Restart Claude Desktop

**Not just closing the window — fully quit and relaunch.**

- **Windows**: System tray (bottom-right) → right-click Claude → **Quit**
- **macOS**: Menu bar → Claude → **Quit** (or `Cmd + Q`)
- **Linux**: Tray → Quit

Then launch Claude Desktop again.

---

## Verify it works

In Claude:
```
Show me Samsung Electronics (005930) current price
```

If you see the stock name, price, and volume, you're done.

<img width="850" height="415" alt="result" src="https://github.com/user-attachments/assets/ac50dd95-85b8-4471-a79c-6aa196f62af4" />

---

## Update

```bash
uv tool upgrade stocklens-mcp
```

Or just re-run the install one-liner (it `--force`-reinstalls).

---

## Diagnose

If install/config seems off:

```bash
stocklens-doctor
```

4-step health check (uv / package / command / config). Each item shows status + fix command.

---

## Troubleshooting

### `uv: command not found`

The uv installer adds `~/.local/bin` to PATH for **new shells**. To keep using the same shell:

**Windows PowerShell:**
```powershell
$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
```

**macOS/Linux:**
```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

### `stocklens-setup: command not found`

Same root cause — PATH not reloaded. Either add `~/.local/bin` to PATH (above) or call by absolute path:

**Windows:**
```powershell
& "$env:USERPROFILE\.local\bin\stocklens-setup.exe"
```

**macOS/Linux:**
```bash
~/.local/bin/stocklens-setup
```

---

### StockLens tools not visible in Claude Desktop

1. Confirm Claude Desktop is fully quit (tray → Quit)
2. Run `stocklens-doctor` to validate the config entry
3. Inspect the config file directly:

**Windows**: File Explorer address bar → `%APPDATA%\Claude`
**macOS**: Finder → `Cmd + Shift + G` → `~/Library/Application Support/Claude`

`claude_desktop_config.json` should contain:

```json
{
  "mcpServers": {
    "stocklens": {
      "command": "C:\\Users\\<you>\\.local\\bin\\stocklens.exe"
    }
  }
}
```

If missing or wrong path:
```bash
stocklens-setup
```

---

### Tools visible but error on invocation

Likely Naver Finance / Yahoo Finance connectivity issue:

1. Check https://finance.naver.com loads in browser
2. Check corporate/school firewall
3. Restart Claude Desktop

---

### Migrating from `naver-stock-mcp` / pip-installed stocklens

Clean up the old pip install first:

```bash
# Windows
py -m pip uninstall naver-stock-mcp stocklens-mcp -y

# macOS/Linux
python3 -m pip uninstall naver-stock-mcp stocklens-mcp -y
```

Then run the one-liner above. `stocklens-setup` updates the existing Claude config entry to the new absolute path.

---

## Still stuck?

Open an issue:
https://github.com/Johnhyeon/stocklens-mcp/issues

Please include:
- OS (Windows/macOS/Linux + version)
- Full `stocklens-doctor` output
- Which step failed
