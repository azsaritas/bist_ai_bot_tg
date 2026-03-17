from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def _read_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    return int(value)


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    telegram_bot_username: str | None
    pollinations_api_key: str | None
    pollinations_model: str
    pollinations_base_url: str
    bot_poll_timeout: int
    request_timeout: int
    app_name: str
    app_public_url: str | None
    github_repo_url: str | None
    app_language: str | None
    discord_contact: str | None
    other_contact: str | None
    tradingview_username: str | None
    tradingview_password: str | None
    tradingview_session: str | None
    tradingview_session_sign: str | None


def get_settings() -> Settings:
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not telegram_bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN tanimli degil.")

    telegram_bot_username = os.getenv("TELEGRAM_BOT_USERNAME", "").strip().lstrip("@") or None
    pollinations_api_key = os.getenv("POLLINATIONS_API_KEY", "").strip() or None
    app_public_url = os.getenv("APP_PUBLIC_URL", "").strip() or None
    if not app_public_url and telegram_bot_username:
        app_public_url = f"https://t.me/{telegram_bot_username}"

    return Settings(
        telegram_bot_token=telegram_bot_token,
        telegram_bot_username=telegram_bot_username,
        pollinations_api_key=pollinations_api_key,
        pollinations_model=os.getenv("POLLINATIONS_MODEL", "gemini-fast").strip() or "gemini-fast",
        pollinations_base_url=os.getenv("POLLINATIONS_BASE_URL", "https://gen.pollinations.ai/v1").strip()
        or "https://gen.pollinations.ai/v1",
        bot_poll_timeout=_read_int("BOT_POLL_TIMEOUT", 30),
        request_timeout=_read_int("REQUEST_TIMEOUT", 60),
        app_name=os.getenv("APP_NAME", "BIST AI Telegram Bot").strip() or "BIST AI Telegram Bot",
        app_public_url=app_public_url,
        github_repo_url=os.getenv("GITHUB_REPO_URL", "").strip() or None,
        app_language=os.getenv("APP_LANGUAGE", "").strip() or None,
        discord_contact=os.getenv("DISCORD_CONTACT", "").strip() or None,
        other_contact=os.getenv("OTHER_CONTACT", "").strip() or None,
        tradingview_username=os.getenv("TRADINGVIEW_USERNAME", "").strip() or None,
        tradingview_password=os.getenv("TRADINGVIEW_PASSWORD", "").strip() or None,
        tradingview_session=os.getenv("TRADINGVIEW_SESSION", "").strip() or None,
        tradingview_session_sign=os.getenv("TRADINGVIEW_SESSION_SIGN", "").strip() or None,
    )
