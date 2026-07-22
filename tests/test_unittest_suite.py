from __future__ import annotations

import json
import os
import sqlite3
import unittest
from pathlib import Path

from src.episode_builder.builder import group_events_into_episodes
from src.episode_builder.models import Episode
from src.feedback import FeedbackStore
from src.graph.graph import AttackGraph
from src.memory.store import EpisodeMemory
from src.normalization.parser import load_json_events
from src.normalization.models import ActivityContext, EntityContext, NormalizedEvent
from src.planner import PlannerAgent
from src.predictor.risk import build_risk_verdict
from src.ttp_mapper.mapper import TtpMatch, select_top_k_ttps
from src.orchestrator.engine import enact_risk_verdict


class TestMapaoPipeline(unittest.TestCase):
    def test_group_events_into_episodes(self):
        path = Path("data/raw/sample_events.json")
        events = load_json_events(path)
        episodes = group_events_into_episodes(events)
        self.assertGreaterEqual(len(episodes), 1)
        self.assertEqual(episodes[0].event_count, len(episodes[0].events))
        self.assertTrue(episodes[0].entity_key)

    def test_episode_memory_save_and_load(self):
        with Path("data/processed").joinpath("test_memory.db").open("w") as _:
            pass
        memory = EpisodeMemory(db_path=Path("data/processed/test_memory.db"))
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
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.event_count, episode.event_count)

    def test_attack_graph_add_episode(self):
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
        self.assertIn("episode-1", graph.graph)
        self.assertIn("evt-001", graph.graph)
        self.assertIn("user1", graph.graph)

        ttp = TtpMatch(
            matched_ttp_id="T1003",
            matched_ttp_name="Credential Dumping",
            ttp_confidence=0.9,
            description="Test technique",
        )
        graph.add_technique(ttp, episode_id="episode-1")
        self.assertIn("T1003", graph.graph)
        self.assertTrue(graph.graph.has_edge("episode-1", "T1003"))

    def test_planner_summary_and_recommendation(self):
        episode = Episode(
            episode_id="episode-1",
            start_time="2026-07-22T12:00:00",
            end_time="2026-07-22T12:10:00",
            entity_key="host:host1",
            events=[
                NormalizedEvent(
                    event_id="evt-001",
                    timestamp="2026-07-22T12:00:00",
                    telemetry_type="endpoint",
                    source_entity=EntityContext(host_id="host1"),
                    activity=ActivityContext(action="process_creation", process_name="cmd.exe"),
                    raw_log_ref="test",
                )
            ],
            event_count=1,
        )
        ttp_match = TtpMatch("T1003", "Credential Dumping", 0.9, "desc")
        verdict = build_risk_verdict(
            episode_id="episode-1",
            ttp_match=ttp_match,
            predicted_next_step="Credential Dumping via Mimikatz",
            asset_criticality=7.0,
            blast_radius=3.0,
            recommended_action="isolate_host",
        )
        planner = PlannerAgent(api_key=None)
        summary = planner.generate_summary(episode, verdict, ttp_match)
        recommendation = planner.generate_containment_recommendation(verdict)
        self.assertIn("Episode episode-1", summary)
        self.assertTrue("action" in recommendation or "analyst" in recommendation)

    def test_select_top_k_ttps(self):
        top_ttps = select_top_k_ttps("test episode summary", k=3)
        self.assertGreaterEqual(len(top_ttps), 1)
        self.assertTrue(top_ttps[0].matched_ttp_id)

    def test_feedback_store(self):
        feedback_store = FeedbackStore(Path("data/processed/unit_feedback.json"))
        feedback_store.add_feedback({"episode_id": "episode-1", "approved": True})
        self.assertIn({"episode_id": "episode-1", "approved": True}, feedback_store.list_feedback())


if __name__ == "__main__":
    unittest.main()
