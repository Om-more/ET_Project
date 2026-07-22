from __future__ import annotations

from src.utils.config import load_policy_config


def determine_confidence_gate(
    overall_score: float,
    blast_radius: float,
) -> str:
    policy = load_policy_config()
    automated_threshold = float(policy.risk.get("automated_confidence", 0.85))
    blast_threshold = float(policy.risk.get("blast_radius_threshold", 4.0))

    if overall_score >= automated_threshold and blast_radius <= blast_threshold:
        return "SOAR_AUTOMATED"
    if overall_score >= automated_threshold and blast_radius > blast_threshold:
        return "HUMAN_APPROVAL"
    return "ANALYST_QUEUE"
