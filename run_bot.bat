@echo off
:: ========================================================
:: Quant Trading Bot Execution Script Wrapper
:: Settings and API keys are managed in .env file.
:: Command-line arguments (%*) are passed directly to Python.
::
:: Behavior:
::   - Double-click (no args): runs --live and pauses to view output.
::   - Scheduled / CLI (with args like --live): executes and exits automatically.
:: ========================================================

cd /d "%~dp0"

if "%~1"=="" (
    python src/main.py --live
    echo.
    echo Execution completed.
    pause
) else (
    python src/main.py %*
    echo.
    echo Execution completed.
)
