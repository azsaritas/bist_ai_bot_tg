from __future__ import annotations

import logging
import time

from bist_bot.ai_service import AICommentaryService, fallback_commentary
from bist_bot.config import Settings, get_settings
from bist_bot.i18n import (
    DEFAULT_LANGUAGE,
    build_ai_model_keyboard,
    build_language_keyboard,
    build_remove_keyboard,
    language_name,
    parse_ai_model_selection,
    parse_language_selection,
    t,
)
from bist_bot.preferences import PreferenceStore
from bist_bot.stock_service import (
    CompanyLookupError,
    build_snapshot,
    configure_tradingview_auth,
    find_company_candidates,
    render_snapshot_message,
)
from bist_bot.telegram_api import TelegramAPIError, TelegramBotClient


LOGGER = logging.getLogger(__name__)


def run() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    settings = get_settings()
    realtime_enabled = False
    try:
        realtime_enabled = configure_tradingview_auth(
            username=settings.tradingview_username,
            password=settings.tradingview_password,
            session=settings.tradingview_session,
            session_sign=settings.tradingview_session_sign,
        )
    except Exception:
        LOGGER.exception("TradingView oturumu acilamadi; varsayilan veri akisina dusuluyor.")

    telegram = TelegramBotClient(settings.telegram_bot_token, timeout=settings.request_timeout)
    ai_service = AICommentaryService(
        api_key=settings.pollinations_api_key,
        base_url=settings.pollinations_base_url,
        model=settings.pollinations_model,
    )
    preferences = PreferenceStore()

    offset: int | None = None
    LOGGER.info("Bot basladi. Realtime etkin: %s", realtime_enabled)

    try:
        while True:
            try:
                updates = telegram.get_updates(offset=offset, timeout=settings.bot_poll_timeout)
                for update in updates:
                    offset = update["update_id"] + 1
                    handle_update(update, telegram, ai_service, realtime_enabled, settings, preferences)
            except KeyboardInterrupt:
                raise
            except Exception:
                LOGGER.exception("Dongu icinde beklenmeyen hata.")
                time.sleep(3)
    finally:
        telegram.close()


def handle_update(
    update: dict,
    telegram: TelegramBotClient,
    ai_service: AICommentaryService,
    realtime_enabled: bool,
    settings: Settings,
    preferences: PreferenceStore,
) -> None:
    message = update.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()
    if not chat_id or not text:
        return

    selected_language = parse_language_selection(text)
    current_language = preferences.get_language(chat_id)
    ui_language = current_language or DEFAULT_LANGUAGE
    pending_action = preferences.get_pending_action(chat_id)
    current_model = preferences.get_ai_model(chat_id) or settings.pollinations_model

    try:
        if selected_language is not None:
            preferences.set_language(chat_id, selected_language)
            preferences.set_pending_action(chat_id, None)
            telegram.send_message(
                chat_id,
                t(selected_language, "language_changed"),
                reply_markup=build_remove_keyboard(),
            )
            selected_or_default_model = preferences.get_ai_model(chat_id) or settings.pollinations_model
            telegram.send_message(chat_id, build_start_text(settings, selected_language, selected_or_default_model))
            return

        selected_model = parse_ai_model_selection(text)
        if pending_action == "aimodel" and selected_model is not None:
            preferences.set_ai_model(chat_id, selected_model)
            preferences.set_pending_action(chat_id, None)
            telegram.send_message(
                chat_id,
                t(ui_language, "ai_model_changed", model=selected_model),
                reply_markup=build_remove_keyboard(),
            )
            telegram.send_message(chat_id, build_start_text(settings, ui_language, selected_model))
            return
        if pending_action == "aimodel" and not text.startswith("/"):
            telegram.send_message(
                chat_id,
                t(ui_language, "invalid_ai_model"),
                reply_markup=build_ai_model_keyboard(),
            )
            return

        if text.startswith("/start"):
            if current_language is None:
                send_language_prompt(chat_id, telegram, ui_language)
                return
            telegram.send_message(chat_id, build_start_text(settings, current_language, current_model))
            return

        if text.startswith("/language"):
            send_language_prompt(chat_id, telegram, ui_language)
            return

        if current_language is None:
            send_language_prompt(chat_id, telegram, ui_language, include_required_notice=True)
            return

        if text.startswith("/help"):
            telegram.send_message(chat_id, build_start_text(settings, current_language, current_model))
            return

        if text.startswith("/about") or text.startswith("/pollinations"):
            telegram.send_message(chat_id, build_about_text(settings, realtime_enabled, current_language, current_model))
            return

        if text.startswith("/aimodel"):
            handle_ai_model_command(chat_id, text, telegram, preferences, settings, current_language)
            return

        if text.startswith("/ara") or text.startswith("/search"):
            query = text.partition(" ")[2].strip()
            handle_search(chat_id, query, telegram, current_language)
            return

        if text.startswith("/hisse") or text.startswith("/stock"):
            query = text.partition(" ")[2].strip()
            if not query:
                telegram.send_message(chat_id, t(current_language, "usage_stock"))
                return
            handle_stock_query(chat_id, query, telegram, ai_service, realtime_enabled, current_language, current_model)
            return

        handle_stock_query(chat_id, text, telegram, ai_service, realtime_enabled, current_language, current_model)
    except TelegramAPIError:
        LOGGER.exception("Telegram mesaji gonderilemedi.")
    except Exception:
        LOGGER.exception("Mesaj islenirken beklenmeyen hata.")
        telegram.send_message(chat_id, t(ui_language, "unexpected_error"))


def send_language_prompt(
    chat_id: int,
    telegram: TelegramBotClient,
    ui_language: str,
    include_required_notice: bool = False,
) -> None:
    lines: list[str] = []
    if include_required_notice:
        lines.append(t(ui_language, "language_required"))
        lines.append("")
    lines.append(t(ui_language, "select_language"))
    telegram.send_message(
        chat_id,
        "\n".join(lines),
        reply_markup=build_language_keyboard(),
    )


def handle_search(chat_id: int, query: str, telegram: TelegramBotClient, language: str) -> None:
    if not query:
        telegram.send_message(chat_id, t(language, "usage_search"))
        return

    candidates = find_company_candidates(query)
    if not candidates:
        telegram.send_message(chat_id, t(language, "no_match"))
        return

    text = t(language, "found_companies") + "\n" + "\n".join(
        f"- {candidate.ticker}: {candidate.name}" for candidate in candidates
    )
    telegram.send_message(chat_id, text)


def handle_ai_model_command(
    chat_id: int,
    text: str,
    telegram: TelegramBotClient,
    preferences: PreferenceStore,
    settings: Settings,
    language: str,
) -> None:
    arg = text.partition(" ")[2].strip()
    available_models = [
        "gemini-fast",
        "claude-airforce",
        "openai-fast",
        "perplexity-fast",
        "step-3.5-flash",
    ]
    if not arg:
        preferences.set_pending_action(chat_id, "aimodel")
        message = "\n".join(
            [
                t(language, "current_ai_model", model=preferences.get_ai_model(chat_id) or settings.pollinations_model),
                t(language, "choose_ai_model"),
                t(language, "available_ai_models"),
                *[f"- {model}" for model in available_models],
            ]
        )
        telegram.send_message(
            chat_id,
            message,
            reply_markup=build_ai_model_keyboard(),
        )
        return

    selected_model = parse_ai_model_selection(arg)
    if selected_model is None:
        telegram.send_message(
            chat_id,
            "\n".join(
                [
                    t(language, "invalid_ai_model"),
                    t(language, "usage_aimodel"),
                    t(language, "available_ai_models"),
                    *[f"- {model}" for model in available_models],
                ]
            ),
        )
        return

    preferences.set_ai_model(chat_id, selected_model)
    preferences.set_pending_action(chat_id, None)
    telegram.send_message(
        chat_id,
        t(language, "ai_model_changed", model=selected_model),
        reply_markup=build_remove_keyboard(),
    )


def handle_stock_query(
    chat_id: int,
    query: str,
    telegram: TelegramBotClient,
    ai_service: AICommentaryService,
    realtime_enabled: bool,
    language: str,
    model: str,
) -> None:
    telegram.send_chat_action(chat_id, "typing")

    try:
        snapshot = build_snapshot(query, realtime_enabled=realtime_enabled)
    except CompanyLookupError as exc:
        if exc.candidates:
            candidates_text = "\n".join(f"- {item.ticker}: {item.name}" for item in exc.candidates)
            telegram.send_message(chat_id, t(language, "ambiguous_header") + "\n" + candidates_text)
            return

        if exc.code == "empty_query":
            telegram.send_message(chat_id, t(language, "empty_query"))
            return

        telegram.send_message(chat_id, t(language, "company_not_found"))
        return
    except Exception:
        LOGGER.exception("Veri toplanirken hata olustu.")
        telegram.send_message(chat_id, t(language, "stock_unavailable"))
        return

    try:
        commentary_title, commentary = ai_service.generate_commentary(snapshot, language, model=model)
    except Exception:
        LOGGER.exception("AI yorumu alinamadi; fallback kullaniliyor.")
        commentary_title, commentary = t(language, "auto_commentary"), fallback_commentary(snapshot, language)

    message = render_snapshot_message(snapshot, commentary_title, commentary, language)
    telegram.send_message(chat_id, message)


def build_start_text(settings: Settings, language: str, active_model: str) -> str:
    lines = [
        t(language, "start_intro", app_name=settings.app_name),
        t(language, "start_body"),
        "",
        t(language, "examples"),
        "/hisse THYAO",
        "/stock THYAO",
        "/hisse Turk Hava Yollari",
        "/search bank",
        "/ara banka",
        "/about",
        "/language",
        "/aimodel",
        "",
        t(language, "start_value", model=active_model),
        t(language, "current_ai_model", model=active_model),
    ]
    if settings.app_public_url:
        lines.extend(["", t(language, "app_link", url=settings.app_public_url)])
    return "\n".join(lines)


def build_about_text(settings: Settings, realtime_enabled: bool, language: str, active_model: str) -> str:
    lines = [
        t(language, "about_app", app_name=settings.app_name),
        t(language, "about_category"),
        t(language, "about_model", model=active_model),
        t(language, "about_api", url=settings.pollinations_base_url),
        t(language, "about_value"),
        t(language, "about_language", lang_name=language_name(language, language)),
        t(language, "about_realtime", status=t(language, "realtime_on" if realtime_enabled else "realtime_off")),
    ]

    if settings.app_public_url:
        lines.append(t(language, "public_app_url", url=settings.app_public_url))
    if settings.github_repo_url:
        lines.append(t(language, "open_source_repo", url=settings.github_repo_url))
    if settings.discord_contact:
        lines.append(t(language, "discord", value=settings.discord_contact))
    if settings.other_contact:
        lines.append(t(language, "contact", value=settings.other_contact))

    lines.extend(["", t(language, "built_with"), t(language, "submission_note")])
    return "\n".join(lines)
