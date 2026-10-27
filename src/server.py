# -*- coding: utf-8 -*-
"""
Crypto Quant Wizard - 올인원 웹 백엔드 & 백그라운드 스케줄러 서버
FastAPI 기반 REST API 및 APScheduler 일체형 서비스
"""

import os
import sys
import json
import logging
import asyncio
import threading
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import requests
import pandas as pd

# 콘솔 UTF-8 인코딩 보장 (Windows CP949 이모지 에러 방지)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# 로컬 모듈 로드
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
from main import execute_bot, get_kst_now
from bithumb_api import BithumbClient
from binance_api import BinanceClient
import pyupbit

# 로그 메모리 버퍼 핸들러 (최근 로그를 웹에 제공)
class MemoryLogHandler(logging.Handler):
    def __init__(self, capacity=500):
        super().__init__()
        self.capacity = capacity
        self.records = []
        self.lock = threading.RLock()

    def emit(self, record):
        try:
            msg = self.format(record)
            with self.lock:
                self.records.append({
                    "timestamp": datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S"),
                    "level": record.levelname,
                    "message": msg
                })
                if len(self.records) > self.capacity:
                    self.records.pop(0)
        except Exception:
            self.handleError(record)

    def get_logs(self, limit=100):
        with self.lock:
            return list(self.records[-limit:])

# 로깅 설정
logger = logging.getLogger("quant_wizard")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")


class SafeStreamHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            try:
                stream.write(msg + self.terminator)
            except UnicodeEncodeError:
                safe_msg = msg.encode("ascii", errors="backslashreplace").decode("ascii")
                stream.write(safe_msg + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

# 콘솔 스트림 핸들러
stream_handler = SafeStreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# 메모리 핸들러 등록 (RLock 적용 및 propagate 방지)
mem_handler = MemoryLogHandler(capacity=500)
mem_handler.setFormatter(formatter)
logger.addHandler(mem_handler)
logger.propagate = False

# 루트 로거에도 안전하게 등록 (중복 방지)
root_logger = logging.getLogger()
if mem_handler not in root_logger.handlers:
    root_logger.addHandler(mem_handler)

from contextlib import asynccontextmanager

# 스케줄러 상태 보관
scheduler = BackgroundScheduler(timezone="Asia/Seoul")
bot_state = {
    "is_running": False,
    "last_run": None,
    "last_result": None,
    "last_status": "idle"
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """서버 수명 주기(시작/종료) 비동기 컨텍스트 매니저"""
    logger.info("==================================================")
    logger.info("[INFO] Crypto Quant Wizard 올인원 서버 시작")
    logger.info("==================================================")
    try:
        hour, minute = [int(x) for x in config.AUTO_SCHEDULE_TIME.strip().split(":")]
    except Exception:
        hour, minute = 9, 5

    scheduler.add_job(
        scheduled_job,
        trigger=CronTrigger(hour=hour, minute=minute, timezone="Asia/Seoul"),
        id="daily_quant_trading",
        replace_existing=True
    )
    scheduler.start()
    if not config.SCHEDULE_ENABLED:
        scheduler.pause_job("daily_quant_trading")
        logger.info("정기 스케줄러가 비활성화(일시정지) 상태로 대기합니다.")
    else:
        logger.info(f"백그라운드 정기 스케줄러 등록 완료: 매일 {hour:02d}:{minute:02d} KST")

    yield

    logger.info("Crypto Quant Wizard 서버 종료 중...")
    if scheduler.running:
        scheduler.shutdown(wait=False)


# FastAPI 앱 생성
app = FastAPI(
    title="Crypto Quant Wizard Server",
    description="3대 거래소 암호화폐 퀀트 봇 웹 매니저 & 일체형 스케줄러",
    version="1.0.0",
    lifespan=lifespan
)

# 기본 경로
BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
DATA_DIR = BASE_DIR / "data"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# [Pydantic 요청 모델]
# ==========================================

class ConfigSaveRequest(BaseModel):
    run_mode: Optional[str] = None
    upbit_strategy: Optional[str] = None
    bithumb_strategy: Optional[str] = None
    binance_strategy: Optional[str] = None
    upbit_access_key: Optional[str] = None
    upbit_secret_key: Optional[str] = None
    bithumb_access_key: Optional[str] = None
    bithumb_secret_key: Optional[str] = None
    binance_access_key: Optional[str] = None
    binance_secret_key: Optional[str] = None
    discord_webhook_url: Optional[str] = None
    schedule_time: Optional[str] = None
    schedule_enabled: Optional[bool] = None


class ExchangeTestRequest(BaseModel):
    exchange: str
    access_key: Optional[str] = None
    secret_key: Optional[str] = None


class DiscordTestRequest(BaseModel):
    webhook_url: str


class RunBotRequest(BaseModel):
    mode: Optional[str] = None


# ==========================================
# [스케줄러 작업 함수]
# ==========================================

def scheduled_job():
    """매일 09:05 KST 정기 실행되는 스케줄러 작업"""
    logger.info("정기 스케줄 트리거: 퀀트 매매 사이클 시작")
    run_bot_task(mode=config.RUN_MODE)


def run_bot_task(mode: Optional[str] = None):
    """봇 실행 백그라운드 작업"""
    global bot_state
    if bot_state["is_running"]:
        logger.warning("이미 봇이 실행 중입니다. 중복 실행을 건너뜁니다.")
        return

    bot_state["is_running"] = True
    bot_state["last_status"] = "running"
    try:
        res = execute_bot(mode=mode)
        bot_state["last_run"] = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M:%S KST")
        bot_state["last_result"] = res
        bot_state["last_status"] = "success" if res.get("success") else "error"
        logger.info(f"봇 실행 완료: {res.get('message')}")
    except Exception as e:
        logger.error(f"봇 실행 중 오류: {e}", exc_info=True)
        bot_state["last_result"] = {"success": False, "message": str(e)}
        bot_state["last_status"] = "error"
    finally:
        bot_state["is_running"] = False


# ==========================================
# [API 엔드포인트]
# ==========================================

@app.get("/api/status")
def get_status():
    """봇 및 스케줄러 현재 상태 조회"""
    next_run = None
    job = scheduler.get_job("daily_quant_trading")
    if job and config.SCHEDULE_ENABLED and job.next_run_time:
        next_run = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S KST")

    # 설정 완료 여부 판정
    public_cfg = config.get_public_config()
    configured_any = (
        public_cfg["upbit"]["configured"] or
        public_cfg["bithumb"]["configured"] or
        public_cfg["binance"]["configured"]
    )

    return {
        "status": "online",
        "bot_state": bot_state,
        "next_run": next_run,
        "schedule_enabled": config.SCHEDULE_ENABLED,
        "schedule_time": config.AUTO_SCHEDULE_TIME,
        "is_configured": configured_any,
        "run_mode": config.RUN_MODE,
        "active_exchanges": {
            "upbit": public_cfg["upbit"]["enabled"],
            "bithumb": public_cfg["bithumb"]["enabled"],
            "binance": public_cfg["binance"]["enabled"]
        }
    }


@app.get("/api/config")
def get_config():
    """공개 가능한 마스킹된 설정 반환"""
    return config.get_public_config()


@app.post("/api/config")
def update_config(payload: ConfigSaveRequest):
    """설정 저장 및 스케줄러 갱신"""
    data = payload.model_dump(exclude_unset=True)
    success = config.save_config(data)
    if not success:
        raise HTTPException(status_code=500, detail="설정 저장 중 오류가 발생했습니다.")

    # 스케줄 시간 및 활성화 상태 갱신
    target_enabled = payload.schedule_enabled if payload.schedule_enabled is not None else config.SCHEDULE_ENABLED
    target_time = payload.schedule_time or config.AUTO_SCHEDULE_TIME
    sync_scheduler_state(target_enabled, target_time)

    return {
        "success": True,
        "message": "설정이 성공적으로 저장되었습니다.",
        "config": config.get_public_config()
    }


@app.post("/api/schedule/toggle")
def toggle_schedule():
    """정기 스케줄러 활성화 / 비활성화(일시정지/삭제) 토글"""
    new_state = not config.SCHEDULE_ENABLED
    config.SCHEDULE_ENABLED = new_state
    config.save_config({"schedule_enabled": new_state})
    sync_scheduler_state(new_state, config.AUTO_SCHEDULE_TIME)
    status_text = "활성화" if new_state else "비활성화(일시정지)"
    return {
        "success": True,
        "schedule_enabled": new_state,
        "message": f"정기 스케줄이 {status_text}되었습니다."
    }


def sync_scheduler_state(enabled: bool, time_str: str = "09:05"):
    """스케줄러 작업 상태(활성화/일시정지/재등록) 동기화"""
    try:
        job = scheduler.get_job("daily_quant_trading")
        hour, minute = [int(x) for x in time_str.strip().split(":")]
        if enabled:
            if not job:
                scheduler.add_job(
                    scheduled_job,
                    trigger=CronTrigger(hour=hour, minute=minute, timezone="Asia/Seoul"),
                    id="daily_quant_trading",
                    replace_existing=True
                )
            else:
                scheduler.reschedule_job(
                    "daily_quant_trading",
                    trigger=CronTrigger(hour=hour, minute=minute, timezone="Asia/Seoul")
                )
                scheduler.resume_job("daily_quant_trading")
            logger.info(f"정기 스케줄러 활성화 완료: 매일 {time_str} KST")
        else:
            if job:
                scheduler.pause_job("daily_quant_trading")
            logger.info("정기 스케줄러가 일시정지(비활성화)되었습니다.")
    except Exception as e:
        logger.warning(f"스케줄러 상태 동기화 실패 ({e})")


def reschedule_job(time_str: str):
    """스케줄러 시간 재설정 (예: '09:05')"""
    try:
        hour, minute = [int(x) for x in time_str.strip().split(":")]
        scheduler.reschedule_job(
            "daily_quant_trading",
            trigger=CronTrigger(hour=hour, minute=minute, timezone="Asia/Seoul")
        )
        logger.info(f"스케줄 시간이 {time_str} KST로 재설정되었습니다.")
    except Exception as e:
        logger.warning(f"스케줄 재설정 실패 ({e}), 기본값 유지")


@app.post("/api/test-exchange")
def test_exchange(payload: ExchangeTestRequest):
    """거래소 API Key 연결 및 잔고 조회 검증"""
    exchange = payload.exchange.lower()
    access_key = payload.access_key or ""
    secret_key = payload.secret_key or ""

    # 마스킹되어 넘어온 경우 기존 설정 키 사용
    if access_key.startswith("••••") or not access_key:
        if exchange == "upbit":
            access_key = config.UPBIT_ACCESS_KEY
            secret_key = secret_key if (secret_key and not secret_key.startswith("••••")) else config.UPBIT_SECRET_KEY
        elif exchange == "bithumb":
            access_key = config.BITHUMB_ACCESS_KEY
            secret_key = secret_key if (secret_key and not secret_key.startswith("••••")) else config.BITHUMB_SECRET_KEY
        elif exchange == "binance":
            access_key = config.BINANCE_ACCESS_KEY
            secret_key = secret_key if (secret_key and not secret_key.startswith("••••")) else config.BINANCE_SECRET_KEY

    if not access_key or not secret_key:
        return {"success": False, "message": "Access Key와 Secret Key를 모두 입력해 주세요."}

    try:
        if exchange == "upbit":
            client = pyupbit.Upbit(access_key, secret_key)
            balances = client.get_balances()
            if isinstance(balances, dict) and "error" in balances:
                return {"success": False, "message": f"업비트 인증 실패: {balances['error'].get('message', balances['error'])}"}
            if not isinstance(balances, list):
                return {"success": False, "message": f"업비트 응답 오류: {balances}"}
            krw_balance = next((float(b["balance"]) for b in balances if b.get("currency") == "KRW"), 0.0)
            coin_count = len([b for b in balances if b.get("currency") != "KRW" and float(b.get("balance", 0)) > 0])
            return {
                "success": True,
                "message": f"업비트 연결 성공! (보유 원화: {krw_balance:,.0f}원, 보유 코인: {coin_count}종)",
                "summary": {"krw": krw_balance, "coins": coin_count}
            }

        elif exchange == "bithumb":
            client = BithumbClient(access_key=access_key, secret_key=secret_key, dry_run=True)
            res = client.get_balances()
            if not isinstance(res, list):
                if isinstance(res, dict) and "error" in res:
                    return {"success": False, "message": f"빗썸 인증 실패: {res['error']}"}
                return {"success": False, "message": f"빗썸 응답 오류: {res}"}
            krw_balance = next((float(b["balance"]) for b in res if b.get("currency") == "KRW"), 0.0)
            coin_count = len([b for b in res if b.get("currency") != "KRW" and float(b.get("balance", 0)) > 0])
            return {
                "success": True,
                "message": f"빗썸 연결 성공! (보유 원화: {krw_balance:,.0f}원, 보유 코인: {coin_count}종)",
                "summary": {"krw": krw_balance, "coins": coin_count}
            }

        elif exchange == "binance":
            client = BinanceClient(access_key=access_key, secret_key=secret_key, dry_run=True)
            bals = client.get_balances()
            usdt_bal = bals.get("USDT", {}).get("free", 0.0)
            btc_bal = bals.get("BTC", {}).get("free", 0.0)
            eth_bal = bals.get("ETH", {}).get("free", 0.0)
            return {
                "success": True,
                "message": f"바이낸스 연결 성공! (USDT: {usdt_bal:,.2f}, BTC: {btc_bal:.6f}, ETH: {eth_bal:.6f})",
                "summary": {"usdt": usdt_bal, "btc": btc_bal, "eth": eth_bal}
            }
        else:
            return {"success": False, "message": f"지원하지 않는 거래소입니다: {exchange}"}

    except Exception as e:
        logger.error(f"{exchange} 연결 테스트 예외 발생: {e}")
        return {"success": False, "message": f"연결 실패 ({type(e).__name__}): {str(e)}"}


@app.post("/api/test-discord")
def test_discord(payload: DiscordTestRequest):
    """디스코드 웹훅 알림 테스트"""
    url = payload.webhook_url.strip()
    if not url:
        return {"success": False, "message": "디스코드 웹훅 URL을 입력해 주세요."}
    if not (url.startswith("https://discord.com/api/webhooks/") or url.startswith("https://discordapp.com/api/webhooks/")):
        return {"success": False, "message": "올바른 디스코드 웹훅 URL 형식이 아닙니다. (https://discord.com/api/webhooks/... 형식이어야 합니다.)"}

    content = {
        "content": "🧙 **[Crypto Quant Wizard]** 디스코드 알림 연동 테스트 성공!\n"
                   f"- 전송 시각: {datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S KST')}\n"
                   "- 알림 채널이 정상적으로 등록되었습니다."
    }
    try:
        resp = requests.post(url, json=content, timeout=8)
        if resp.status_code in [200, 204]:
            return {"success": True, "message": "디스코드 테스트 알림이 성공적으로 전송되었습니다."}
        else:
            return {"success": False, "message": f"전송 실패 (상태 코드: {resp.status_code}): {resp.text}"}
    except Exception as e:
        return {"success": False, "message": f"전송 오류: {str(e)}"}


@app.post("/api/run-now")
def run_now(payload: Optional[RunBotRequest] = None, background_tasks: BackgroundTasks = None):
    """사용자 요청에 의한 즉시 실행 (백그라운드 스레드)"""
    if bot_state["is_running"]:
        return JSONResponse(
            status_code=409,
            content={"success": False, "message": "현재 봇이 매매 사이클을 실행 중입니다. 잠시 후 다시 시도해 주세요."}
        )

    mode = payload.mode if payload and payload.mode else config.RUN_MODE
    threading.Thread(target=run_bot_task, kwargs={"mode": mode}, daemon=True).start()
    return {"success": True, "message": f"[{mode}] 모드로 봇 실행이 시작되었습니다. 잠시 후 결과가 갱신됩니다."}


@app.get("/api/logs")
def get_logs(limit: int = 150):
    """최근 실행 로그 반환"""
    return {"logs": mem_handler.get_logs(limit=limit)}


@app.get("/api/data/status")
def get_dashboard_status():
    """대시보드 상태 데이터 (docs/data/status.json) 반환"""
    status_path = DOCS_DIR / "data" / "status.json"
    if status_path.exists():
        try:
            with open(status_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "holdings" not in data:
                    data["holdings"] = {
                        "btc": {"total_quantity": 0, "total_val_krw": 0},
                        "eth": {"total_quantity": 0, "total_val_krw": 0},
                        "cash": {"total_krw": 0, "upbit_krw": 0, "bithumb_krw": 0, "binance_usdt": 0}
                    }
                return data
        except Exception as e:
            logger.warning(f"status.json 로드 실패 ({e})")
    
    # status.json이 없으면 기본 구조 반환
    return {
        "updated_at": datetime.now(timezone(timedelta(hours=9))).isoformat(),
        "mode": config.RUN_MODE,
        "holdings": {
            "btc": {"total_quantity": 0, "total_val_krw": 0},
            "eth": {"total_quantity": 0, "total_val_krw": 0},
            "cash": {"total_krw": 0, "upbit_krw": 0, "bithumb_krw": 0, "binance_usdt": 0}
        },
        "guides": {
            "upbit": "시작 대기 중",
            "bithumb": "시작 대기 중",
            "binance": "시작 대기 중"
        },
        "chart": []
    }


@app.get("/api/data/trades")
def get_trades(limit: int = 50):
    """거래 체결 장부 반환"""
    trade_path = DATA_DIR / "trade_history.csv"
    if trade_path.exists():
        try:
            df = pd.read_csv(trade_path)
            records = df.tail(limit).to_dict(orient="records")
            records.reverse()
            return {"trades": records}
        except Exception as e:
            logger.warning(f"trade_history.csv 로드 실패 ({e})")
    return {"trades": []}


@app.get("/api/data/assets")
def get_assets(limit: int = 60):
    """자산 추이 데이터 반환"""
    asset_path = DATA_DIR / "asset_history.csv"
    if asset_path.exists():
        try:
            df = pd.read_csv(asset_path)
            records = df.tail(limit).to_dict(orient="records")
            return {"assets": records}
        except Exception as e:
            logger.warning(f"asset_history.csv 로드 실패 ({e})")
    return {"assets": []}


# 정적 파일 마운트 (docs 디렉토리)
if DOCS_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(DOCS_DIR)), name="static")

@app.get("/")
def serve_index():
    """메인 웹페이지 서빙"""
    index_path = DOCS_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Crypto Quant Wizard Server Running"}


if __name__ == "__main__":
    port = config.WEB_PORT
    logger.info(f"웹 서비스 시작: http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
