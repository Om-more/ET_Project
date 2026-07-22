from __future__ import annotations

from src.planner import PlannerAgent
from src.episode_builder.models import Episode
from src.normalization.models import ActivityContext, EntityContext, NormalizedEvent
from src.ttp_mapper.mapper import TtpMatch
from src.predictor.risk import build_risk_verdict


def test_planner_generates_summaries():
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
    assert "Episode episode-1" in summary
    assert "automated action" in recommendation or "analyst" in recommendation
