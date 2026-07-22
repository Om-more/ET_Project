from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.utils.config import get_project_root


class FeedbackStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or get_project_root() / "data" / "processed" / "feedback.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as handle:
            try:
                return json.load(handle)
            except json.JSONDecodeError:
                return []

    def add_feedback(self, feedback: dict[str, Any]) -> None:
        existing = self._load()
        existing.append(feedback)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(existing, handle, indent=2)

    def list_feedback(self) -> list[dict[str, Any]]:
        return self._load()
