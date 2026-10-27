@echo off
chcp 65001 >nul
title Crypto Quant Wizard

set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"

echo ========================================================
echo   Crypto Quant Wizard All-in-One Launcher
echo   3 Exchanges Crypto Quant Trading Bot and Dashboard
echo ========================================================
echo.

cd /d "%~dp0"

REM 1. Python Check
set "PY_CMD="
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py"
) else (
    where python >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "PY_CMD=python"
    )
)

if "%PY_CMD%"=="" (
    echo [ERROR] Python not found.
    echo Please install Python 3.10+ from https://www.python.org
    pause
    exit /b 1
)

REM 2. Virtualenv Check and Creation
if not exist ".venv\Scripts\activate.bat" (
    echo [1/3] Creating virtual environment .venv...
    %PY_CMD% -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM 3. Activate and Install Requirements
call .venv\Scripts\activate.bat
if not exist ".venv\installed.flag" (
    echo [2/3] Installing dependencies for the first time...
    python -m pip install -r requirements.txt
    if %ERRORLEVEL% equ 0 (
        echo installed > .venv\installed.flag
    ) else (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
) else (
    echo [2/3] Dependencies verified.
)

REM 4. Launch Browser and Web Server
echo.
echo [3/3] Starting Web Manager and Daily 09:05 KST Scheduler!
echo Web Dashboard URL: http://localhost:8080
echo (To stop the server, press Ctrl+C in this window)
echo ========================================================
echo.

start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:8080"

python src\server.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Server exited with an error code: %ERRORLEVEL%
    pause
)
pause
