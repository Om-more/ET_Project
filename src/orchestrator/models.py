from __future__ import annotations

from pydantic import BaseModel


class RiskVerdict(BaseModel):
    episode_id: str
    matched_ttp_id: str
    matched_ttp_name: str
    ttp_confidence: float
    predicted_next_step: str
    asset_criticality: float
    blast_radius: float
    overall_risk_score: float
    recommended_action: str
    gate_decision: str
    explanation: str | None = None
