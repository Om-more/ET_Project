from __future__ import annotations

from src.orchestrator.models import RiskVerdict
from src.ttp_mapper.mapper import TtpMatch
from src.utils.config import load_policy_config


def compute_overall_risk_score(ttp_confidence: float, asset_criticality: float, blast_radius: float) -> float:
    return ttp_confidence * ((asset_criticality + blast_radius) / 2.0)


def determine_gate_decision(confidence: float, blast_radius: float) -> str:
    policy = load_policy_config()
    automated_threshold = float(policy.risk["automated_confidence"])
    blast_threshold = float(policy.risk["blast_radius_threshold"])

    if confidence >= automated_threshold and blast_radius <= blast_threshold:
        return "SOAR_AUTOMATED"
    if confidence >= automated_threshold and blast_radius > blast_threshold:
        return "HUMAN_APPROVAL"
    return "ANALYST_QUEUE"


def build_risk_verdict(
    episode_id: str,
    ttp_match: TtpMatch,
    predicted_next_step: str,
    asset_criticality: float,
    blast_radius: float,
    recommended_action: str,
) -> RiskVerdict:
    overall = compute_overall_risk_score(ttp_match.ttp_confidence, asset_criticality, blast_radius)
    gate_decision = determine_gate_decision(ttp_match.ttp_confidence, blast_radius)

    return RiskVerdict(
        episode_id=episode_id,
        matched_ttp_id=ttp_match.matched_ttp_id,
        matched_ttp_name=ttp_match.matched_ttp_name,
        ttp_confidence=ttp_match.ttp_confidence,
        predicted_next_step=predicted_next_step,
        asset_criticality=asset_criticality,
        blast_radius=blast_radius,
        overall_risk_score=overall,
        recommended_action=recommended_action,
        gate_decision=gate_decision,
    )
