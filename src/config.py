# -*- coding: utf-8 -*-
"""
전역 환경 설정 및 거래소-전략 파라미터 관리 모듈
.env 및 data/config.json을 통합 지원하며, 거래소와 전략을 분리하여 관리합니다.
"""

import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv, set_key

# 기본 경로
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_JSON_PATH = DATA_DIR / "config.json"
ENV_PATH = BASE_DIR / ".env"

# .env 로드
load_dotenv(dotenv_path=ENV_PATH)

def load_json_config():
    """data/config.json 파일이 존재하면 로드합니다."""
    if CONFIG_JSON_PATH.exists():
        try:
            with open(CONFIG_JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.warning(f"config.json 로드 실패 ({e}), .env 설정을 우선 적용합니다.")
    return {}

_json_cfg = load_json_config()

# ==========================================
# [시스템 제어 및 환경 설정]
# ==========================================

IS_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS", "").lower() == "true"

# 운용 모드: 'live', 'dry_run', 'signal' (기본값: dry_run)
_raw_mode = os.getenv("RUN_MODE", _json_cfg.get("run_mode", "dry_run")).lower().replace("-", "_")
if _raw_mode in ["live", "dry_run", "signal"]:
    RUN_MODE = _raw_mode
else:
    RUN_MODE = "dry_run"

# 하위 호환성 불리언 플래그
SIGNAL_ONLY = IS_GITHUB_ACTIONS or (RUN_MODE == "signal") or (os.getenv("SIGNAL_ONLY", "false").lower() == "true")
DRY_RUN = True if SIGNAL_ONLY else (RUN_MODE == "dry_run" or (os.getenv("DRY_RUN", "false").lower() == "true"))

# ==========================================
# [거래소별 전략 매핑 (Decoupled Mapping)]
# ==========================================
# 업비트 전략: 'dual_momentum_5050', 'none'
UPBIT_STRATEGY = os.getenv("UPBIT_STRATEGY", _json_cfg.get("upbit_strategy", "dual_momentum_5050"))
USE_UPBIT_STRATEGY = UPBIT_STRATEGY != "none"

# 빗썸 전략: 'eth_supertrend', 'dual_momentum_5050', 'none'
BITHUMB_STRATEGY = os.getenv("BITHUMB_STRATEGY", _json_cfg.get("bithumb_strategy", "eth_supertrend"))
USE_BITHUMB_STRATEGY = BITHUMB_STRATEGY != "none"
USE_ALTCOIN_STRATEGY = USE_BITHUMB_STRATEGY  # 하위 호환 별칭

# 바이낸스 전략: 'dual_momentum_5050', 'none'
BINANCE_STRATEGY = os.getenv("BINANCE_STRATEGY", _json_cfg.get("binance_strategy", "dual_momentum_5050"))
USE_BINANCE_STRATEGY = BINANCE_STRATEGY != "none"

# ==========================================
# [보안 정보 설정] - API 키 및 디스코드 주소
# ==========================================
UPBIT_ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY", _json_cfg.get("upbit_access_key", ""))
UPBIT_SECRET_KEY = os.getenv("UPBIT_SECRET_KEY", _json_cfg.get("upbit_secret_key", ""))

BITHUMB_ACCESS_KEY = os.getenv("BITHUMB_ACCESS_KEY", _json_cfg.get("bithumb_access_key", ""))
BITHUMB_SECRET_KEY = os.getenv("BITHUMB_SECRET_KEY", _json_cfg.get("bithumb_secret_key", ""))

BINANCE_ACCESS_KEY = os.getenv("BINANCE_ACCESS_KEY", os.getenv("BINANCE_API_KEY", _json_cfg.get("binance_access_key", "")))
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", os.getenv("BINANCE_SECRET", _json_cfg.get("binance_secret_key", "")))

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", _json_cfg.get("discord_webhook_url", ""))

# 자동 푸시 활성화 여부 (오픈소스 기본값: False)
ENABLE_GIT_AUTO_PUSH = os.getenv("ENABLE_GIT_AUTO_PUSH", "false").lower() == "true"

# 웹 서버 포트 및 스케줄 시간
WEB_PORT = int(os.getenv("WEB_PORT", _json_cfg.get("web_port", 8080)))
AUTO_SCHEDULE_TIME = os.getenv("AUTO_SCHEDULE_TIME", _json_cfg.get("auto_schedule_time", "09:05"))

# ==========================================
# [전략 세부 운용 상수]
# ==========================================
BTC_SMA_LEN = 220
ETH_SMA_LEN = 50

BINANCE_BTC_SMA_LEN = 200
BINANCE_BTC_BUFFER = 0.02
BINANCE_ETH_SMA_LEN = 40
BINANCE_ETH_ATR_MULTIPLIER = 1.2

MAIN_RATIO_BAND = 0.10
ETH_ATR_MULTIPLIER = 1.5
BTC_BUFFER = 0.02

UPBIT_MIN_ORDER_KRW = 5000
BITHUMB_MIN_ORDER_KRW = 5000
BINANCE_MIN_ORDER_USDT = 5.0


def mask_key(key: str) -> str:
    """API 키의 중간부를 마스킹하여 반환합니다."""
    if not key:
        return ""
    if len(key) <= 8:
        return "••••••••"
    return f"{key[:4]}••••••••{key[-4:]}"


def get_public_config() -> dict:
    """웹 UI에 안전하게 전달할 수 있는 설정 딕셔너리를 반환합니다."""
    return {
        "run_mode": RUN_MODE,
        "upbit": {
            "enabled": bool(UPBIT_ACCESS_KEY and UPBIT_SECRET_KEY and USE_UPBIT_STRATEGY),
            "configured": bool(UPBIT_ACCESS_KEY and UPBIT_SECRET_KEY),
            "access_key_masked": mask_key(UPBIT_ACCESS_KEY),
            "has_secret": bool(UPBIT_SECRET_KEY),
            "strategy": UPBIT_STRATEGY
        },
        "bithumb": {
            "enabled": bool(BITHUMB_ACCESS_KEY and BITHUMB_SECRET_KEY and USE_BITHUMB_STRATEGY),
            "configured": bool(BITHUMB_ACCESS_KEY and BITHUMB_SECRET_KEY),
            "access_key_masked": mask_key(BITHUMB_ACCESS_KEY),
            "has_secret": bool(BITHUMB_SECRET_KEY),
            "strategy": BITHUMB_STRATEGY
        },
        "binance": {
            "enabled": bool(BINANCE_ACCESS_KEY and BINANCE_SECRET_KEY and USE_BINANCE_STRATEGY),
            "configured": bool(BINANCE_ACCESS_KEY and BINANCE_SECRET_KEY),
            "access_key_masked": mask_key(BINANCE_ACCESS_KEY),
            "has_secret": bool(BINANCE_SECRET_KEY),
            "strategy": BINANCE_STRATEGY
        },
        "discord": {
            "configured": bool(DISCORD_WEBHOOK_URL),
            "webhook_masked": mask_key(DISCORD_WEBHOOK_URL)
        },
        "web_port": WEB_PORT,
        "schedule_time": AUTO_SCHEDULE_TIME
    }


def save_config(new_config: dict) -> bool:
    """
    사용자가 웹 마법사/설정 화면에서 제출한 설정을 .env 및 config.json에 영구 저장하고 전역 변수를 갱신합니다.
    """
    global RUN_MODE, DRY_RUN, SIGNAL_ONLY
    global UPBIT_STRATEGY, USE_UPBIT_STRATEGY, BITHUMB_STRATEGY, USE_BITHUMB_STRATEGY, USE_ALTCOIN_STRATEGY, BINANCE_STRATEGY, USE_BINANCE_STRATEGY
    global UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY, BITHUMB_ACCESS_KEY, BITHUMB_SECRET_KEY, BINANCE_ACCESS_KEY, BINANCE_SECRET_KEY
    global DISCORD_WEBHOOK_URL, WEB_PORT, AUTO_SCHEDULE_TIME

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. 운용 모드 갱신
    if "run_mode" in new_config and new_config["run_mode"]:
        RUN_MODE = new_config["run_mode"].lower().replace("-", "_")
        DRY_RUN = RUN_MODE == "dry_run"
        SIGNAL_ONLY = RUN_MODE == "signal"
        set_key(str(ENV_PATH), "RUN_MODE", RUN_MODE)
        set_key(str(ENV_PATH), "DRY_RUN", "true" if DRY_RUN else "false")
        set_key(str(ENV_PATH), "SIGNAL_ONLY", "true" if SIGNAL_ONLY else "false")

    # 2. 거래소별 전략 매핑 갱신
    if "upbit_strategy" in new_config:
        UPBIT_STRATEGY = new_config["upbit_strategy"]
        USE_UPBIT_STRATEGY = UPBIT_STRATEGY != "none"
        set_key(str(ENV_PATH), "UPBIT_STRATEGY", UPBIT_STRATEGY)

    if "bithumb_strategy" in new_config:
        BITHUMB_STRATEGY = new_config["bithumb_strategy"]
        USE_BITHUMB_STRATEGY = BITHUMB_STRATEGY != "none"
        USE_ALTCOIN_STRATEGY = USE_BITHUMB_STRATEGY
        set_key(str(ENV_PATH), "BITHUMB_STRATEGY", BITHUMB_STRATEGY)

    if "binance_strategy" in new_config:
        BINANCE_STRATEGY = new_config["binance_strategy"]
        USE_BINANCE_STRATEGY = BINANCE_STRATEGY != "none"
        set_key(str(ENV_PATH), "BINANCE_STRATEGY", BINANCE_STRATEGY)

    # 3. API 키 갱신 (빈 문자열이거나 마스킹 형태가 아닌 실제 변경값일 때만 갱신)
    def update_key(key_name, val):
        if val is not None and not val.startswith("••••") and val.strip() != "":
            set_key(str(ENV_PATH), key_name, val.strip())
            return val.strip()
        return os.getenv(key_name, "")

    if "upbit_access_key" in new_config:
        UPBIT_ACCESS_KEY = update_key("UPBIT_ACCESS_KEY", new_config["upbit_access_key"])
    if "upbit_secret_key" in new_config:
        UPBIT_SECRET_KEY = update_key("UPBIT_SECRET_KEY", new_config["upbit_secret_key"])

    if "bithumb_access_key" in new_config:
        BITHUMB_ACCESS_KEY = update_key("BITHUMB_ACCESS_KEY", new_config["bithumb_access_key"])
    if "bithumb_secret_key" in new_config:
        BITHUMB_SECRET_KEY = update_key("BITHUMB_SECRET_KEY", new_config["bithumb_secret_key"])

    if "binance_access_key" in new_config:
        BINANCE_ACCESS_KEY = update_key("BINANCE_ACCESS_KEY", new_config["binance_access_key"])
    if "binance_secret_key" in new_config:
        BINANCE_SECRET_KEY = update_key("BINANCE_SECRET_KEY", new_config["binance_secret_key"])

    if "discord_webhook_url" in new_config:
        DISCORD_WEBHOOK_URL = update_key("DISCORD_WEBHOOK_URL", new_config["discord_webhook_url"])

    # 4. config.json 동기화 저장
    save_dict = {
        "run_mode": RUN_MODE,
        "upbit_strategy": UPBIT_STRATEGY,
        "bithumb_strategy": BITHUMB_STRATEGY,
        "binance_strategy": BINANCE_STRATEGY,
        "web_port": WEB_PORT,
        "auto_schedule_time": AUTO_SCHEDULE_TIME
    }
    with open(CONFIG_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(save_dict, f, ensure_ascii=False, indent=2)

    logging.info("설정이 .env 및 config.json에 성공적으로 저장되었습니다.")
    return True
