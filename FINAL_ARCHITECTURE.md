# FINAL_ARCHITECTURE

## MAPAO Architecture Overview

The repository implements a modular cyber resilience pipeline with a fixed stage structure:

- Telemetry Ingestion
- Normalization
- Episode Builder
- Episode Memory
- Behavior Model
- MITRE Mapping
- Next-Step Prediction
- Risk Engine
- Decision Fusion
- Confidence Gate
- Planner
- SOAR
- Dashboard
- Feedback

## Core Components

- `src/normalization/`: Converts raw JSON events into `NormalizedEvent` objects.
- `src/episode_builder/`: Groups events into episodes by user/host/session/IP/time window.
- `src/memory/`: Persists episodes to a SQLite backend with versioning and search.
- `src/graph/`: Builds an attack graph using NetworkX for users, hosts, IPs, processes, and ATT&CK techniques.
- `src/predictor/`: Contains risk scoring, decision fusion, confidence gating, and model interfaces.
- `src/planner.py`: Generates analyst-friendly summaries and containment recommendations.
- `src/orchestrator/`: Simulates SOAR actions and audit logging.
- `src/feedback.py`: Stores analyst feedback for future retraining.
- `src/rag/`: Builds and loads a FAISS-backed MITRE index.
- `src/ttp_mapper/`: Matches episodes to ATT&CK techniques.
- `training/`: Provides scripts to train the behavior model, TTP classifier, and next-step predictor.

## Runtime Entry Points

- `api/main.py`: FastAPI analysis endpoint.
- `dashboards/streamlit_app.py`: Streamlit dashboard UI.
- `scripts/build_mitre_rag.py`: MITRE index builder.

## Data Flow

1. Raw events are loaded from `data/raw/`.
2. Events are normalized into entity and activity contexts.
3. Normalized events are grouped into episodes.
4. Episodes are stored in SQLite and appended to an attack graph.
5. Episode summary text is matched to MITRE techniques.
6. The risk verdict is computed using behavior, TTP, planner, asset, and blast radius signals.
7. The confidence gate chooses between automated SOAR, human approval, or analyst queue.
8. The planner creates natural-language summaries and containment recommendations.
9. Feedback is recorded for analyst actions.
10. Results are exposed through API and dashboard layers.
