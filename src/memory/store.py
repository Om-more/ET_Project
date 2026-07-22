from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Iterator

from pydantic import BaseModel

from src.episode_builder.models import Episode

DEFAULT_DB_FILE = "data/processed/episode_memory.db"


def get_default_memory_db() -> Path:
    root = Path(__file__).resolve().parents[2]
    return root / DEFAULT_DB_FILE


class EpisodeMemory(BaseModel):
    db_path: Path

    def __init__(self, db_path: Path | None = None):
        db_path = db_path or get_default_memory_db()
        db_path.parent.mkdir(parents=True, exist_ok=True)
        object.__setattr__(self, "db_path", db_path)
        self._connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        cursor = self._connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS episodes (
                episode_id TEXT NOT NULL,
                version INTEGER NOT NULL,
                entity_key TEXT,
                start_time TEXT,
                end_time TEXT,
                event_count INTEGER,
                event_json TEXT,
                created_at TEXT,
                PRIMARY KEY(episode_id, version)
            )
            """
        )
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_entity_key ON episodes(entity_key)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON episodes(created_at)")
        self._connection.commit()

    def save_episode(self, episode: Episode, version: int = 1) -> None:
        created_at = datetime.utcnow().isoformat() + "Z"
        event_json = episode.json()
        cursor = self._connection.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO episodes (
                episode_id,
                version,
                entity_key,
                start_time,
                end_time,
                event_count,
                event_json,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                episode.episode_id,
                version,
                episode.entity_key,
                episode.start_time,
                episode.end_time,
                episode.event_count,
                event_json,
                created_at,
            ),
        )
        self._connection.commit()

    def get_episode(self, episode_id: str, version: int | None = None) -> Episode | None:
        cursor = self._connection.cursor()
        if version is None:
            cursor.execute(
                "SELECT * FROM episodes WHERE episode_id = ? ORDER BY version DESC LIMIT 1",
                (episode_id,),
            )
        else:
            cursor.execute(
                "SELECT * FROM episodes WHERE episode_id = ? AND version = ?",
                (episode_id, version),
            )
        row = cursor.fetchone()
        if row is None:
            return None
        payload = json.loads(row["event_json"])
        return Episode.parse_obj(payload)

    def list_episodes(
        self,
        entity_key: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Episode]:
        cursor = self._connection.cursor()
        if entity_key:
            cursor.execute(
                "SELECT * FROM episodes WHERE entity_key = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (entity_key, limit, offset),
            )
        else:
            cursor.execute(
                "SELECT * FROM episodes ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset),
            )
        rows = cursor.fetchall()
        return [Episode.parse_obj(json.loads(row["event_json"])) for row in rows]

    def search_episodes(self, query: str, limit: int = 50) -> list[Episode]:
        cursor = self._connection.cursor()
        pattern = f"%{query}%"
        cursor.execute(
            "SELECT * FROM episodes WHERE event_json LIKE ? OR entity_key LIKE ? ORDER BY created_at DESC LIMIT ?",
            (pattern, pattern, limit),
        )
        rows = cursor.fetchall()
        return [Episode.parse_obj(json.loads(row["event_json"])) for row in rows]

    def get_versions(self, episode_id: str) -> list[int]:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT version FROM episodes WHERE episode_id = ? ORDER BY version DESC",
            (episode_id,),
        )
        return [int(row["version"]) for row in cursor.fetchall()]

    def close(self) -> None:
        self._connection.close()
