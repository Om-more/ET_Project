from __future__ import annotations

from src.orchestrator.models import RiskVerdict
from src.ttp_mapper.mapper import TtpMatch
from src.predictor.confidence_gate import determine_confidence_gate
from src.predictor.decision_fusion import compute_final_threat_score, build_decision_explanation


def compute_overall_risk_score(
    behavior_score: float,
    ttp_confidence: float,
    planner_confidence: float,
    asset_criticality: float,
    blast_radius: float,
) -> float:
    return compute_final_threat_score(
        behavior_score=behavior_score,
        ttp_confidence=ttp_confidence,
        planner_confidence=planner_confidence,
        asset_criticality=asset_criticality,
        blast_radius=blast_radius,
    )


def build_risk_verdict(
    episode_id: str,
    ttp_match: TtpMatch,
    predicted_next_step: str,
    asset_criticality: float,
    blast_radius: float,
    recommended_action: str,
    behavior_score: float = 0.5,
    planner_confidence: float = 0.5,
) -> RiskVerdict:
    overall = compute_overall_risk_score(
        behavior_score=behavior_score,
        ttp_confidence=ttp_match.ttp_confidence,
        planner_confidence=planner_confidence,
        asset_criticality=asset_criticality,
        blast_radius=blast_radius,
    )
    gate_decision = determine_confidence_gate(overall, blast_radius)
    explanation = build_decision_explanation(
        behavior_score=behavior_score,
        ttp_confidence=ttp_match.ttp_confidence,
        planner_confidence=planner_confidence,
        asset_criticality=asset_criticality,
        blast_radius=blast_radius,
        gate_decision=gate_decision,
    )

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
        explanation=explanation,
    )
