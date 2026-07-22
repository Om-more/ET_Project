from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.rag.indexer import get_default_indexer


@dataclass
class TtpMatch:
    matched_ttp_id: str
    matched_ttp_name: str
    ttp_confidence: float
    description: str
    evidence: str | None = None


def select_top_k_ttps(episode_text: str, k: int = 3) -> list[TtpMatch]:
    indexer = get_default_indexer()
    candidates = indexer.retrieve_top_k(episode_text, k=k)
    if not candidates:
        raise ValueError("No MITRE techniques retrieved")

    return [
        TtpMatch(
            matched_ttp_id=item["id"],
            matched_ttp_name=item["name"],
            ttp_confidence=min(max(float(item["score"]), 0.0), 1.0),
            description=item.get("description", ""),
            evidence=item.get("text"),
        )
        for item in candidates
    ]


def select_best_ttp(episode_text: str, k: int = 3) -> TtpMatch:
    matches = select_top_k_ttps(episode_text, k=k)
    return max(matches, key=lambda item: item.ttp_confidence)
