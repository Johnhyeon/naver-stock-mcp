#!/bin/bash
# StockLens Update (macOS / Linux)

set -e

GREEN='\033[0;32m'
NC='\033[0m'

echo "=============================================="
echo "  StockLens Update"
echo "=============================================="
echo ""

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "Updating to latest version..."
$PYTHON_CMD -m pip install --upgrade stocklens-mcp
echo ""
echo -e "${GREEN}✓ Update complete!${NC}"
echo ""
echo "Please restart Claude Desktop."
echo ""
