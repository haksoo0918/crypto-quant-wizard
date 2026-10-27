# -*- coding: utf-8 -*-
"""
디스코드 웹훅 알림 발송 모듈
"""
import json
import logging
import requests
from typing import Optional

try:
    from config import DISCORD_WEBHOOK_URL
except ImportError:
    try:
        from src.config import DISCORD_WEBHOOK_URL
    except ImportError:
        DISCORD_WEBHOOK_URL = ""


def send_discord_message(content: str, webhook_url: Optional[str] = None) -> bool:
    """
    디스코드 채널로 텍스트 메시지를 전송합니다.
    webhook_url이 주어지지 않으면 설정 파일의 DISCORD_WEBHOOK_URL을 사용합니다.
    """
    url = webhook_url or DISCORD_WEBHOOK_URL
    if not url:
        logging.warning("디스코드 웹훅 URL이 설정되어 있지 않습니다. 알림 전송을 건너뜁니다.")
        return False

    payload = {"content": content}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
        if response.status_code in (200, 204):
            logging.info("디스코드 알림 발송 성공")
            return True
        else:
            logging.error(f"디스코드 알림 발송 실패 (상태 코드: {response.status_code}): {response.text}")
            return False
    except Exception as e:
        logging.error(f"디스코드 알림 발송 중 예외 발생: {e}")
        return False


def make_bold(text: str) -> str:
    return f"**{text}**"


def make_code(text: str) -> str:
    return f"`{text}`"
