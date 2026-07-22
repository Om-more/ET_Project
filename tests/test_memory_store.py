from __future__ import annotations

from pathlib import Path

from src.episode_builder.models import Episode
from src.memory.store import EpisodeMemory
from src.normalization.models import ActivityContext, EntityContext, NormalizedEvent


def test_episode_memory_save_and_load(tmp_path: Path):
    memory = EpisodeMemory(db_path=tmp_path / "memory.db")
    event = NormalizedEvent(
        event_id="evt-test",
        timestamp="2026-07-22T12:00:00",
        telemetry_type="endpoint",
        source_entity=EntityContext(host_id="host1"),
        activity=ActivityContext(action="test_action"),
        raw_log_ref="test",
    )
    episode = Episode(
        episode_id="episode-1",
        start_time="2026-07-22T12:00:00",
        end_time="2026-07-22T12:01:00",
        entity_key="host:host1",
        events=[event],
        event_count=1,
    )

    memory.save_episode(episode)
    loaded = memory.get_episode("episode-1")
    assert loaded is not None
    assert loaded.episode_id == episode.episode_id
    assert loaded.event_count == episode.event_count
