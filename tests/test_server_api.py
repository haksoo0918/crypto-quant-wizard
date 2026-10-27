# -*- coding: utf-8 -*-
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import config
import server
from server import ConfigSaveRequest, ExchangeTestRequest


def test_api_status():
    status = server.get_status()
    assert status["status"] == "online"
    assert "bot_state" in status
    assert "run_mode" in status
    assert "active_exchanges" in status


def test_api_config():
    cfg = server.get_config()
    assert "run_mode" in cfg
    assert "upbit" in cfg
    assert "bithumb" in cfg
    assert "binance" in cfg
    assert "discord" in cfg


def test_api_config_update():
    req = ConfigSaveRequest(
        run_mode="dry_run",
        upbit_strategy="dual_momentum_5050",
        bithumb_strategy="eth_supertrend",
        binance_strategy="dual_momentum_5050"
    )
    res = server.update_config(req)
    assert res["success"] is True
    assert res["config"]["run_mode"] == "dry_run"
    assert res["config"]["upbit"]["strategy"] == "dual_momentum_5050"


def test_api_logs():
    res = server.get_logs(limit=10)
    assert "logs" in res
    assert isinstance(res["logs"], list)


def test_api_dashboard_status():
    data = server.get_dashboard_status()
    assert "mode" in data
    assert "holdings" in data
    assert "guides" in data


def test_test_exchange_empty():
    req = ExchangeTestRequest(exchange="upbit", access_key="", secret_key="")
    res = server.test_exchange(req)
    assert res["success"] is False
    assert "Key를 모두 입력" in res["message"]


def test_test_discord_invalid():
    # 빈 URL
    req_empty = server.DiscordTestRequest(webhook_url="")
    res_empty = server.test_discord(req_empty)
    assert res_empty["success"] is False

    # 잘못된 URL 형식
    req_bad = server.DiscordTestRequest(webhook_url="https://google.com/bad")
    res_bad = server.test_discord(req_bad)
    assert res_bad["success"] is False
    assert "형식이 아닙니다" in res_bad["message"]


def test_test_exchange_invalid_credentials():
    req = ExchangeTestRequest(exchange="upbit", access_key="invalid_test_key", secret_key="invalid_test_secret")
    res = server.test_exchange(req)
    assert res["success"] is False
    assert "실패" in res["message"] or "오류" in res["message"]


def test_serve_index_exists():
    index_file = server.DOCS_DIR / "index.html"
    assert index_file.exists()
    content = index_file.read_text(encoding="utf-8")
    assert "Crypto Quant Wizard" in content
    assert "설정 마법사" in content
    assert "대시보드" in content
