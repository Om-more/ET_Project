from __future__ import annotations


def normalize(value: float, maximum: float) -> float:
    if maximum <= 0:
        return 0.0
    return min(max(value / maximum, 0.0), 1.0)


def compute_final_threat_score(
    behavior_score: float,
    ttp_confidence: float,
    planner_confidence: float,
    asset_criticality: float,
    blast_radius: float,
) -> float:
    normalized_behavior = normalize(behavior_score, 1.0)
    normalized_ttp = normalize(ttp_confidence, 1.0)
    normalized_planner = normalize(planner_confidence, 1.0)
    normalized_asset = normalize(asset_criticality, 10.0)
    normalized_blast = normalize(blast_radius, 10.0)

    weights = {
        "behavior": 0.25,
        "ttp": 0.25,
        "planner": 0.2,
        "asset": 0.15,
        "blast": 0.15,
    }

    score = (
        normalized_behavior * weights["behavior"]
        + normalized_ttp * weights["ttp"]
        + normalized_planner * weights["planner"]
        + normalized_asset * weights["asset"]
        + normalized_blast * weights["blast"]
    )

    return min(max(score, 0.0), 1.0)


def build_decision_explanation(
    behavior_score: float,
    ttp_confidence: float,
    planner_confidence: float,
    asset_criticality: float,
    blast_radius: float,
    gate_decision: str,
) -> str:
    return (
        f"Decision fusion combined behavior={behavior_score:.2f}, ttp_confidence={ttp_confidence:.2f}, "
        f"planner_confidence={planner_confidence:.2f}, asset_criticality={asset_criticality:.1f}, "
        f"blast_radius={blast_radius:.1f} into gate_decision={gate_decision}."
    )
