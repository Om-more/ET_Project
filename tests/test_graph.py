from __future__ import annotations

from src.graph.graph import AttackGraph
from src.ttp_mapper.mapper import TtpMatch
from src.episode_builder.models import Episode
from src.normalization.models import ActivityContext, EntityContext, NormalizedEvent


def test_attack_graph_add_episode():
    graph = AttackGraph()
    event = NormalizedEvent(
        event_id="evt-001",
        timestamp="2026-07-22T12:00:00",
        telemetry_type="endpoint",
        source_entity=EntityContext(host_id="host1", user_id="user1", ip="10.0.0.1"),
        activity=ActivityContext(action="process_creation", process_name="cmd.exe"),
        raw_log_ref="test",
    )
    episode = Episode(
        episode_id="episode-1",
        start_time="2026-07-22T12:00:00",
        end_time="2026-07-22T12:01:00",
        entity_key="user:user1",
        events=[event],
        event_count=1,
    )
    graph.add_episode(episode)
    assert "episode-1" in graph.graph
    assert "evt-001" in graph.graph
    assert "user1" in graph.graph

    ttp = TtpMatch(
        matched_ttp_id="T1003",
        matched_ttp_name="Credential Dumping",
        ttp_confidence=0.9,
        description="Test technique",
    )
    graph.add_technique(ttp, episode_id="episode-1")
    assert "T1003" in graph.graph
    assert graph.graph.has_edge("episode-1", "T1003")
