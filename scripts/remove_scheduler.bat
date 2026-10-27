@echo off
setlocal
chcp 65001 > nul

echo =======================================================
echo  Crypto Quant Wizard - 윈도우 작업 스케줄러 삭제
echo =======================================================
echo.

set "TASK_NAME=CryptoQuantWizard"
set "LEGACY_TASK=QuantCryptoLiveTrader"

echo 작업 스케줄러에서 등록된 봇을 삭제합니다...
echo.

schtasks /delete /tn "%TASK_NAME%" /f > nul 2>&1
set "RES1=%ERRORLEVEL%"

schtasks /delete /tn "%LEGACY_TASK%" /f > nul 2>&1
set "RES2=%ERRORLEVEL%"

if %RES1% equ 0 (
    echo [성공] %TASK_NAME% 작업이 윈도우 스케줄러에서 완전히 삭제되었습니다.
) else if %RES2% equ 0 (
    echo [성공] %LEGACY_TASK% 작업이 윈도우 스케줄러에서 완전히 삭제되었습니다.
) else (
    echo [안내] 등록된 작업 스케줄이 없거나 이미 삭제되었습니다.
)

echo.
echo =======================================================
echo  삭제가 완료되었습니다.
echo =======================================================
echo.
pause
