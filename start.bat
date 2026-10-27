@echo off
chcp 65001 >nul
title Crypto Quant Wizard

echo ========================================================
echo   🧙 Crypto Quant Wizard 올인원 런처 시작
echo   3대 거래소 암호화폐 퀀트 봇 & 대시보드
echo ========================================================
echo.

cd /d "%~dp0"

:: 1. Python 설치 확인
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py"
) else (
    where python >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "PY_CMD=python"
    ) else (
        echo [ERROR] Python이 설치되어 있지 않습니다.
        echo https://www.python.org 에서 Python 3.10 이상을 설치해 주세요.
        pause
        exit /b 1
    )
)

:: 2. 가상환경(.venv) 확인 및 생성
if not exist ".venv\Scripts\activate.bat" (
    echo [1/3] 가상환경(.venv)을 생성합니다...
    %PY_CMD% -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] 가상환경 생성 실패
        pause
        exit /b 1
    )
)

:: 3. 가상환경 활성화 및 패키지 설치
echo [2/3] 필수 패키지 의존성을 점검하고 설치합니다...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [ERROR] 패키지 설치 중 오류가 발생했습니다.
    pause
    exit /b 1
)

:: 4. 브라우저 자동 오픈 및 웹 서버 실행
echo.
echo [3/3] 퀀트 웹 매니저 및 09:05 백그라운드 스케줄러를 시작합니다!
echo 접속 주소: http://localhost:8080
echo (종료하려면 이 창에서 Ctrl+C를 누르세요)
echo ========================================================
echo.

:: 2초 후 브라우저 오픈 (백그라운드)
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:8080"

:: 서버 실행
python src\server.py
pause
