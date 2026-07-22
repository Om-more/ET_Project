from __future__ import annotations

from pathlib import Path

from src.episode_builder.builder import group_events_into_episodes
from src.normalization.parser import load_json_events


def test_group_events_into_episodes():
    path = Path("data/raw/sample_events.json")
    events = load_json_events(path)
    episodes = group_events_into_episodes(events)
    assert len(episodes) >= 1
    assert episodes[0].event_count == len(episodes[0].events)
    assert episodes[0].entity_key
