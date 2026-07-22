from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.episode_builder.builder import build_episode_summary, group_events_into_episodes
from src.feedback import FeedbackStore
from src.graph.graph import AttackGraph
from src.normalization.parser import load_json_events
from src.planner import PlannerAgent
from src.predictor.risk import build_risk_verdict
from src.memory.store import EpisodeMemory
from src.ttp_mapper.mapper import select_best_ttp, select_top_k_ttps
from src.orchestrator.engine import enact_risk_verdict

app = FastAPI(title="MAPAO API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze")
def analyze_events(file_path: str):
    events = load_json_events(Path(file_path))
    episodes = group_events_into_episodes(events)
    results = []

    memory = EpisodeMemory()
    graph = AttackGraph()
    planner = PlannerAgent()
    feedback = FeedbackStore()

    for episode in episodes:
        memory.save_episode(episode)
        graph.add_episode(episode)

        summary = build_episode_summary(episode)
        top_ttps = select_top_k_ttps(summary, k=3)
        ttp_match = top_ttps[0]
        graph.add_technique(ttp_match, episode_id=episode.episode_id)

        verdict = build_risk_verdict(
            episode_id=episode.episode_id,
            ttp_match=ttp_match,
            predicted_next_step="Credential Dumping via Mimikatz",
            asset_criticality=5.0,
            blast_radius=3.5,
            recommended_action="isolate_host",
        )
        action = enact_risk_verdict(verdict, entity_identifier=episode.entity_key.split(":", 1)[-1])
        planner_summary = planner.generate_summary(episode, verdict, ttp_match)
        planner_recommendation = planner.generate_containment_recommendation(verdict)
        feedback.add_feedback(
            {
                "episode_id": episode.episode_id,
                "gate_decision": verdict.gate_decision,
                "feedback_created_at": verdict.episode_id,
                "predicted_next_step": verdict.predicted_next_step,
            }
        )
        results.append({
            "episode": episode.dict(),
            "top_ttps": [ttp.__dict__ for ttp in top_ttps],
            "ttp_match": ttp_match.__dict__,
            "verdict": verdict.dict(),
            "planned_summary": planner_summary,
            "planned_recommendation": planner_recommendation,
            "action": action,
        })

    return {"results": results}
