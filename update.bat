@echo off
setlocal

echo ==============================================
echo   StockLens Update
echo ==============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed.
    pause
    exit /b 1
)

echo Updating to latest version...
python -m pip install --upgrade stocklens-mcp
if errorlevel 1 (
    echo Update failed.
    pause
    exit /b 1
)

echo.
echo ==============================================
echo   Update complete!
echo ==============================================
echo.
echo Please restart Claude Desktop.
echo.
pause
