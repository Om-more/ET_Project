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


def select_best_ttp(episode_text: str, k: int = 3) -> TtpMatch:
    indexer = get_default_indexer()
    candidates = indexer.retrieve_top_k(episode_text, k=k)
    if not candidates:
        raise ValueError("No MITRE techniques retrieved")

    best = max(candidates, key=lambda item: item["score"])
    confidence = float(best["score"])

    return TtpMatch(
        matched_ttp_id=best["id"],
        matched_ttp_name=best["name"],
        ttp_confidence=min(max(confidence, 0.0), 1.0),
        description=best.get("description", ""),
    )
