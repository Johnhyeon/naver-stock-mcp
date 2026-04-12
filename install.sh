#!/bin/bash
# StockLens Installer (macOS / Linux)

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=============================================="
echo "  StockLens Installer"
echo "=============================================="
echo ""

if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
else
    OS="Unknown"
fi
echo "  Detected OS: $OS"
echo ""

# [1/3] Python
echo "[1/3] Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "      ${RED}✗ Python not installed.${NC}"
    echo ""
    echo "      Install Python 3.11+ first:"
    if [[ "$OS" == "macOS" ]]; then
        echo "        brew install python"
    else
        echo "        sudo apt install python3 python3-pip"
    fi
    exit 1
fi

PYVER=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "      ${GREEN}✓ Python $PYVER found${NC}"

PYMAJOR=$(echo $PYVER | cut -d. -f1)
PYMINOR=$(echo $PYVER | cut -d. -f2)
if [ "$PYMAJOR" -lt 3 ] || ([ "$PYMAJOR" -eq 3 ] && [ "$PYMINOR" -lt 11 ]); then
    echo -e "      ${YELLOW}⚠ Python 3.11+ required (current: $PYVER)${NC}"
    exit 1
fi
echo ""

# [2/3] Install
echo "[2/3] Installing stocklens-mcp..."
if $PYTHON_CMD -m pip install --upgrade stocklens-mcp > /tmp/stocklens-install.log 2>&1; then
    echo -e "      ${GREEN}✓ stocklens-mcp installed${NC}"
else
    echo -e "      ${RED}✗ Installation failed${NC}"
    echo "      Log: /tmp/stocklens-install.log"
    exit 1
fi
echo ""

# [3/3] Configure
echo "[3/3] Configuring Claude Desktop..."
$PYTHON_CMD -m stock_mcp_server.setup_claude stocklens
echo ""

echo "=============================================="
echo "  Installation complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "  1. Quit Claude Desktop completely."
if [[ "$OS" == "macOS" ]]; then
    echo "     (Cmd+Q or Menu > Quit)"
fi
echo "  2. Restart Claude Desktop."
echo "  3. Try: \"Samsung Electronics current price\""
echo ""
