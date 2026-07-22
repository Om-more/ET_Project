# PROJECT_ANALYSIS

## Overview

MAPAO is a modular cyber resilience platform that processes telemetry events through normalization, episode construction, MITRE ATT&CK mapping, risk scoring, and simulated SOAR actions. The repository is organized into a simple pipeline with API, dashboard, and RAG index build entry points.

## Repository Structure

- `api/main.py`
  - FastAPI service exposing `/health` and `/analyze` routes.
- `dashboards/streamlit_app.py`
  - Streamlit dashboard for loading raw events, viewing episodes, and reviewing risk verdicts.
- `scripts/build_mitre_rag.py`
  - Builds the MITRE RAG index from STIX JSON data.
- `configs/policies.yaml`
  - Policy-driven configuration for risk thresholds, asset criticality, and audit logging.
- `data/raw/`
  - Raw telemetry and MITRE STIX data inputs used by runtime and build scripts.
- `src/`
  - Core pipeline modules.

## Core Package Responsibilities

- `src/normalization/`
  - Parses raw event JSON into normalized event objects.
  - Defines entity and activity contexts.
- `src/episode_builder/`
  - Groups normalized events into structured episodes.
  - Builds human-readable episode summaries.
- `src/ttp_mapper/`
  - Matches episodes to MITRE techniques using a vector index.
- `src/rag/`
  - Builds and loads the MITRE RAG index.
- `src/predictor/`
  - Computes risk verdicts and gate decisions.
- `src/orchestrator/`
  - Simulates SOAR action enforcement and audit logging.
- `src/utils/`
  - Loads configuration and policy settings.

## Data Flow

1. Receive raw telemetry from `data/raw/sample_events.json`.
2. Normalize raw events into `NormalizedEvent` objects.
3. Group events into episodes by user/host/session/IP/time window.
4. Summarize episodes as narrative text.
5. Retrieve best matching ATT&CK techniques via the MITRE RAG index.
6. Score risk and determine gate decisions based on policy thresholds.
7. Simulate SOAR actions and audit the decision.
8. Present results through API and dashboard interfaces.

## Known Gaps and Missing Implementation

- The project currently lacks the following modules requested by the prompt:
  - `src/memory/`
  - `src/graph/`
  - Extended `src/predictor/` models (`behavior_model.py`, `ttp_classifier.py`, `next_step_predictor.py`)
  - Training scripts under `training/`
- A package import mismatch exists between `mapao.src.*` and the actual `src/` package layout.

## Broken Import Path

- Entry points and some internal imports use `mapao.src.*`.
- The repository source code is located in top-level `src/` and not nested under `mapao/src/`.
- This mismatch prevents the dashboard and build script from importing modules correctly.

## Immediate Runtime Dependencies

The repository depends on the following runtime packages:

- `fastapi`
- `streamlit`
- `pyyaml`
- `pydantic`
- `faiss-cpu`
- `sentence-transformers`

## Notes

- No syntax errors exist in the current codebase.
- The dashboard and build script imports must be fixed before runtime.
- No tests currently exist in `tests/`.
- The data folder contains sample telemetry and MITRE STIX JSON.
