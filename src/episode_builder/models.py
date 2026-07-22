from __future__ import annotations

from typing import List

from pydantic import BaseModel

from src.normalization.models import NormalizedEvent


class Episode(BaseModel):
    episode_id: str
    start_time: str
    end_time: str
    entity_key: str
    events: List[NormalizedEvent]
    event_count: int
