@echo off
setlocal
chcp 65001 > nul

echo =======================================================
echo  Crypto Quant Wizard - 윈도우 작업 스케줄러 등록
echo =======================================================
echo.
echo 대상 작업: 부팅/로그온 시 Crypto Quant Wizard 자동 실행
echo 실행 파일: start.bat
echo.

set "TASK_NAME=CryptoQuantWizard"
for %%I in ("%~dp0..") do set "PROJECT_ROOT=%%~fI"
set "BAT_PATH=%PROJECT_ROOT%\start.bat"

if not exist "%BAT_PATH%" (
    echo [오류] start.bat 파일을 찾을 수 없습니다: %BAT_PATH%
    pause
    exit /b 1
)

echo 스케줄러 작업 등록 중: %TASK_NAME%
echo 실행 경로: %BAT_PATH%
echo.

schtasks /create /f /tn "%TASK_NAME%" /sc onlogon /tr "\"%BAT_PATH%\""

if %ERRORLEVEL% equ 0 (
    echo.
    echo =======================================================
    echo [성공] 윈도우 작업 스케줄러에 성공적으로 등록되었습니다!
    echo PC에 로그인할 때마다 봇과 웹 대시보드가 자동 실행됩니다.
    echo =======================================================
) else (
    echo.
    echo [오류] 작업 등록에 실패했습니다.
    echo 관리자 권한으로 다시 실행해 주세요 (마우스 우클릭 -> 관리자 권한으로 실행).
)

echo.
pause
