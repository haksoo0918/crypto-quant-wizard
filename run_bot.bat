@echo off
:: ========================================================
:: Quant Trading Bot Execution Script Wrapper
:: Settings and API keys are managed in .env file.
:: Command-line arguments (%*) are passed directly to Python.
::
:: Behavior:
::   - Double-click (no args): runs safe dry-run analysis and pauses.
::   - Live execution: run with --live (e.g., 'run_bot.bat --live').
:: ========================================================

cd /d "%~dp0"

if "%~1"=="" (
    echo [안내] 인자가 지정되지 않아 안전 분석 모드(Dry-run)로 1회 실행합니다.
    echo 실거래 주문을 원하시면 'run_bot.bat --live' 로 실행하십시오.
    echo.
    python src/main.py
    echo.
    echo 실행이 완료되었습니다.
    pause
) else (
    python src/main.py %*
    echo.
    echo 실행이 완료되었습니다.
)
