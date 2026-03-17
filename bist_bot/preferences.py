from __future__ import annotations

import json
from pathlib import Path


class PreferenceStore:
    def __init__(self, path: str = "data/chat_preferences.json") -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._write({})

    def get_language(self, chat_id: int) -> str | None:
        data = self._read()
        value = data.get(str(chat_id), {})
        language = value.get("language")
        return language if isinstance(language, str) else None

    def set_language(self, chat_id: int, language: str) -> None:
        data = self._read()
        entry = data.setdefault(str(chat_id), {})
        entry["language"] = language
        self._write(data)

    def get_ai_model(self, chat_id: int) -> str | None:
        data = self._read()
        value = data.get(str(chat_id), {})
        model = value.get("ai_model")
        return model if isinstance(model, str) else None

    def set_ai_model(self, chat_id: int, model: str) -> None:
        data = self._read()
        entry = data.setdefault(str(chat_id), {})
        entry["ai_model"] = model
        self._write(data)

    def get_pending_action(self, chat_id: int) -> str | None:
        data = self._read()
        value = data.get(str(chat_id), {})
        action = value.get("pending_action")
        return action if isinstance(action, str) else None

    def set_pending_action(self, chat_id: int, action: str | None) -> None:
        data = self._read()
        entry = data.setdefault(str(chat_id), {})
        if action is None:
            entry.pop("pending_action", None)
        else:
            entry["pending_action"] = action
        self._write(data)

    def _read(self) -> dict:
        try:
            return json.loads(self._path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _write(self, data: dict) -> None:
        self._path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
