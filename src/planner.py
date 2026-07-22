from __future__ import annotations

import os
from typing import Optional

from src.episode_builder.models import Episode
from src.ttp_mapper.mapper import TtpMatch
from src.predictor.risk import RiskVerdict


class PlannerAgent:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.enabled = bool(self.api_key)

    def generate_summary(self, episode: Episode, verdict: RiskVerdict, ttp_match: TtpMatch) -> str:
        if self.enabled:
            return self._format_summary(episode, verdict, ttp_match, use_llm=True)
        return self._format_summary(episode, verdict, ttp_match, use_llm=False)

    def generate_containment_recommendation(self, verdict: RiskVerdict) -> str:
        if self.enabled:
            return self._format_recommendation(verdict, use_llm=True)
        return self._format_recommendation(verdict, use_llm=False)

    def _format_summary(self, episode: Episode, verdict: RiskVerdict, ttp_match: TtpMatch, use_llm: bool) -> str:
        text = (
            f"Episode {episode.episode_id} on {episode.entity_key} from {episode.start_time} to {episode.end_time}. "
            f"This episode contains {episode.event_count} events and is mapped to ATT&CK technique {ttp_match.matched_ttp_id} ({ttp_match.matched_ttp_name}) "
            f"with confidence {ttp_match.ttp_confidence:.2f}. The system computed an overall risk score of {verdict.overall_risk_score:.2f} "
            f"and gate decision {verdict.gate_decision}."
        )
        if use_llm:
            return f"[GROQ synopsis enabled] {text} Provide analyst-friendly incident context and containment rationale."
        return text

    def _format_recommendation(self, verdict: RiskVerdict, use_llm: bool) -> str:
        if verdict.gate_decision == "SOAR_AUTOMATED":
            recommendation = f"Execute automated action: {verdict.recommended_action}."
        elif verdict.gate_decision == "HUMAN_APPROVAL":
            recommendation = "Recommend analyst review and approval before containment."
        else:
            recommendation = "Escalate to the analyst queue for further investigation."

        if use_llm:
            return f"[GROQ recommendation enabled] {recommendation} Outline the next steps in natural language."
        return recommendation
