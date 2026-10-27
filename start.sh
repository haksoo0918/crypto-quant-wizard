#!/usr/bin/env bash
# ========================================================
# 🧙 Crypto Quant Wizard 올인원 런처 (Linux / Mac / Oracle Cloud)
# ========================================================

set -e
cd "$(dirname "$0")"

echo "========================================================"
echo "  🧙 Crypto Quant Wizard 올인원 런처 시작"
echo "  3대 거래소 암호화폐 퀀트 봇 & 대시보드"
echo "========================================================"

# 1. Python3 설치 확인
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3이 설치되어 있지 않습니다."
    echo "Ubuntu/Debian: sudo apt update && sudo apt install -y python3 python3-venv python3-pip"
    exit 1
fi

# 2. 가상환경(.venv) 확인 및 생성
if [ ! -d ".venv" ]; then
    echo "[1/3] 가상환경(.venv)을 생성합니다..."
    python3 -m venv .venv
fi

# 3. 가상환경 활성화 및 패키지 설치
echo "[2/3] 가상환경 활성화 및 필수 패키지 설치..."
source .venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

# 4. 웹 서버 및 백그라운드 스케줄러 실행
echo ""
echo "[3/3] 퀀트 웹 매니저 및 09:05 백그라운드 스케줄러를 시작합니다!"
echo "접속 주소: http://0.0.0.0:8080"
echo "오라클 클라우드 VM에서는 브라우저로 http://<서버_공인_IP>:8080 으로 접속하세요."
echo "백그라운드 24시간 실행 명령어: nohup ./start.sh > server.log 2>&1 &"
echo "========================================================"
echo ""

# GUI 환경인 경우 브라우저 열기 시도 (Mac: open, Linux: xdg-open)
if command -v xdg-open &> /dev/null; then
    (sleep 2 && xdg-open "http://localhost:8080") &
elif command -v open &> /dev/null; then
    (sleep 2 && open "http://localhost:8080") &
fi

python3 src/server.py
