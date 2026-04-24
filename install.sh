#!/bin/bash
# StockLens Installer (macOS / Linux)
# Usage:
#   curl -LsSf https://raw.githubusercontent.com/Johnhyeon/stocklens-mcp/main/install.sh | sh
#
# 3 steps:
#   1) uv (Python package manager) — auto-installs Python runtime if missing
#   2) stocklens-mcp via `uv tool install`
#   3) Claude Desktop config via `stocklens-setup`

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
else
    OS="Unknown"
fi

echo ""
echo "=============================================="
echo "  StockLens Installer ($OS)"
echo "=============================================="
echo ""

LOCAL_BIN="$HOME/.local/bin"

# ── [1/3] uv ─────────────────────────────────────────────
echo -e "${CYAN}[1/3] Checking uv...${NC}"
if ! command -v uv > /dev/null 2>&1; then
    echo "      uv not found. Installing from astral.sh..."
    if ! curl -LsSf https://astral.sh/uv/install.sh | sh; then
        echo -e "      ${RED}[FAIL] uv installation failed.${NC}"
        echo "      Manual install: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
    # uv installer adds ~/.local/bin to PATH for new shells. Patch this session.
    if [ -d "$LOCAL_BIN" ]; then
        export PATH="$LOCAL_BIN:$PATH"
    fi
    if ! command -v uv > /dev/null 2>&1; then
        echo -e "      ${RED}[FAIL] uv installed but not on PATH. Open a new terminal and re-run.${NC}"
        exit 1
    fi
    echo -e "      ${GREEN}uv installed: $(command -v uv)${NC}"
else
    echo -e "      ${GREEN}uv found: $(command -v uv)${NC}"
fi
echo ""

# ── [2/3] stocklens-mcp ──────────────────────────────────
echo -e "${CYAN}[2/3] Installing stocklens-mcp...${NC}"

# Remove legacy pip-installed package if present (avoids dual-registration confusion)
for PYBIN in python3 python; do
    if command -v "$PYBIN" > /dev/null 2>&1; then
        if "$PYBIN" -m pip show naver-stock-mcp > /dev/null 2>&1; then
            echo "      Removing legacy naver-stock-mcp (system pip)..."
            "$PYBIN" -m pip uninstall -y naver-stock-mcp > /dev/null 2>&1 || true
        fi
        break
    fi
done

# --force re-creates the tool environment, so re-running upgrades cleanly.
if ! uv tool install --force stocklens-mcp; then
    echo -e "      ${RED}[FAIL] uv tool install failed.${NC}"
    exit 1
fi
echo -e "      ${GREEN}stocklens-mcp installed via uv tool${NC}"
echo ""

# Ensure ~/.local/bin is on PATH for the rest of this session
case ":$PATH:" in
    *":$LOCAL_BIN:"*) ;;
    *) [ -d "$LOCAL_BIN" ] && export PATH="$LOCAL_BIN:$PATH" ;;
esac

# ── [3/3] Claude Desktop config ──────────────────────────
echo -e "${CYAN}[3/3] Configuring Claude Desktop...${NC}"
if [ -x "$LOCAL_BIN/stocklens-setup" ]; then
    "$LOCAL_BIN/stocklens-setup" stocklens
else
    uv tool run --from stocklens-mcp stocklens-setup stocklens
fi
echo ""

# ── Verify ───────────────────────────────────────────────
echo -e "${CYAN}Verifying installation...${NC}"
if [ -x "$LOCAL_BIN/stocklens-doctor" ]; then
    if ! "$LOCAL_BIN/stocklens-doctor"; then
        echo ""
        echo -e "${RED}[FAIL] Doctor reported critical issues. See above for fix commands.${NC}"
        exit 1
    fi
else
    if ! uv tool run --from stocklens-mcp stocklens-doctor; then
        echo ""
        echo -e "${RED}[FAIL] Doctor reported critical issues.${NC}"
        exit 1
    fi
fi
echo ""

echo "=============================================="
echo -e "${GREEN}  Installation complete${NC}"
echo "=============================================="
echo ""
echo "Next steps:"
echo "  1. Fully quit Claude Desktop"
if [[ "$OS" == "macOS" ]]; then
    echo "     (Cmd+Q or menu bar -> Claude -> Quit)"
fi
echo "  2. Restart Claude Desktop"
echo "  3. Try: '삼성전자 현재가'"
echo ""
echo "Update later:  uv tool upgrade stocklens-mcp"
echo "Diagnose:      stocklens-doctor"
echo ""
