@echo off
chcp 65001 >nul 2>nul
setlocal

echo ==============================================
echo   naver-stock-mcp Update
echo ==============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed.
    pause
    exit /b 1
)

echo Updating to latest version...
python -m pip install --upgrade naver-stock-mcp
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
