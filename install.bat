@echo off
setlocal EnableDelayedExpansion

echo ==============================================
echo   StockLens Installer (Windows)
echo ==============================================
echo.

REM [1/3] Find Python
echo [1/3] Checking Python...

set "PYTHON_CMD="

python --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python"
    goto :found_python
)

python3 --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python3"
    goto :found_python
)

py -3 --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=py -3"
    goto :found_python
)

for %%P in (
    "%LOCALAPPDATA%\Programs\Python\Python315\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "C:\Python315\python.exe"
    "C:\Python314\python.exe"
    "C:\Python313\python.exe"
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
) do (
    if exist %%P (
        set "PYTHON_CMD=%%~P"
        goto :found_python
    )
)

echo       [FAIL] Python is not installed.
echo.
echo       Please install Python 3.11+ first:
echo       https://www.python.org/downloads/
echo.
echo       IMPORTANT: Check "Add Python to PATH" during installation.
echo.
pause
exit /b 1

:found_python
for /f "tokens=*" %%v in ('!PYTHON_CMD! --version 2^>^&1') do set PYVER=%%v
echo       [OK] %PYVER% found
echo       Using: !PYTHON_CMD!
echo.

REM [2/3] Install stocklens-mcp from PyPI
echo [2/3] Installing stocklens-mcp...
!PYTHON_CMD! -m pip install --upgrade stocklens-mcp
if errorlevel 1 (
    echo       [FAIL] Package installation failed.
    echo       Try: %PYTHON_CMD% -m pip install --upgrade stocklens-mcp
    echo.
    pause
    exit /b 1
)
echo       [OK] stocklens-mcp installed
echo.

REM [3/3] Configure Claude Desktop
echo [3/3] Configuring Claude Desktop...
!PYTHON_CMD! -m stock_mcp_server.setup_claude stocklens
if errorlevel 1 (
    echo       [FAIL] Claude Desktop configuration failed.
    pause
    exit /b 1
)
echo.

echo ==============================================
echo   Installation complete!
echo ==============================================
echo.
echo Next steps:
echo   1. Quit Claude Desktop completely.
echo      (Right-click tray icon, then Quit)
echo   2. Restart Claude Desktop.
echo   3. Try asking: "Samsung Electronics current price"
echo.
pause
