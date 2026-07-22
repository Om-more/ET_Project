from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.episode_builder.builder import build_episode_summary, group_events_into_episodes
from src.normalization.parser import load_json_events
from src.predictor.risk import build_risk_verdict
from src.ttp_mapper.mapper import select_best_ttp
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

    for episode in episodes:
        summary = build_episode_summary(episode)
        ttp_match = select_best_ttp(summary)
        verdict = build_risk_verdict(
            episode_id=episode.episode_id,
            ttp_match=ttp_match,
            predicted_next_step="Credential Dumping via Mimikatz",
            asset_criticality=5.0,
            blast_radius=3.5,
            recommended_action="isolate_host",
        )
        action = enact_risk_verdict(verdict, entity_identifier=episode.entity_key.split(":", 1)[-1])
        results.append({
            "episode": episode.dict(),
            "ttp_match": ttp_match.__dict__,
            "verdict": verdict.dict(),
            "action": action,
        })

    return {"results": results}
