from __future__ import annotations

from typing import Any

import httpx


class TelegramAPIError(RuntimeError):
    """Raised when Telegram Bot API returns an error."""


class TelegramBotClient:
    def __init__(self, token: str, timeout: int = 60) -> None:
        self._base_url = f"https://api.telegram.org/bot{token}"
        self._client = httpx.Client(timeout=timeout)

    def close(self) -> None:
        self._client.close()

    def _post(self, method: str, payload: dict[str, Any]) -> Any:
        response = self._client.post(f"{self._base_url}/{method}", json=payload)
        response.raise_for_status()

        data = response.json()
        if not data.get("ok"):
            description = data.get("description", "Telegram istegi basarisiz oldu.")
            raise TelegramAPIError(description)
        return data["result"]

    def get_updates(self, offset: int | None, timeout: int) -> list[dict[str, Any]]:
        payload: dict[str, Any] = {
            "timeout": timeout,
            "allowed_updates": ["message"],
        }
        if offset is not None:
            payload["offset"] = offset
        return self._post("getUpdates", payload)

    def send_chat_action(self, chat_id: int, action: str = "typing") -> None:
        self._post("sendChatAction", {"chat_id": chat_id, "action": action})

    def send_message(
        self,
        chat_id: int,
        text: str,
        reply_markup: dict[str, Any] | None = None,
    ) -> None:
        chunks = _chunk_text(text)
        for index, chunk in enumerate(chunks):
            payload: dict[str, Any] = {
                "chat_id": chat_id,
                "text": chunk,
            }
            if index == 0 and reply_markup is not None:
                payload["reply_markup"] = reply_markup
            self._post("sendMessage", payload)


def _chunk_text(text: str, max_length: int = 3900) -> list[str]:
    if len(text) <= max_length:
        return [text]

    chunks: list[str] = []
    remaining = text
    while len(remaining) > max_length:
        split_at = remaining.rfind("\n\n", 0, max_length)
        if split_at == -1:
            split_at = remaining.rfind("\n", 0, max_length)
        if split_at == -1:
            split_at = remaining.rfind(" ", 0, max_length)
        if split_at == -1:
            split_at = max_length

        chunks.append(remaining[:split_at].strip())
        remaining = remaining[split_at:].strip()

    if remaining:
        chunks.append(remaining)

    return chunks
