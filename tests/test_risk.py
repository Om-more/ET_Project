from __future__ import annotations

from src.predictor.risk import build_risk_verdict
from src.ttp_mapper.mapper import TtpMatch


def test_build_risk_verdict_contains_explanation():
    ttp_match = TtpMatch(
        matched_ttp_id="T1003",
        matched_ttp_name="Credential Dumping",
        ttp_confidence=0.9,
        description="Test technique",
    )
    verdict = build_risk_verdict(
        episode_id="episode-1",
        ttp_match=ttp_match,
        predicted_next_step="Credential Dumping via Mimikatz",
        asset_criticality=7.0,
        blast_radius=3.0,
        recommended_action="isolate_host",
    )
    assert verdict.explanation is not None
    assert "gate_decision" in verdict.explanation
