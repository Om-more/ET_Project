# CHANGELOG

## Unreleased

### Added

- `src/memory/` module with SQLite-backed episode persistence, search, and versioning.
- `src/graph/` module using NetworkX to model users, hosts, IPs, processes, episodes, and ATT&CK techniques.
- `src/predictor/behavior_model.py` with Isolation Forest training, load, save, and predict interfaces.
- `src/predictor/ttp_classifier.py` with XGBoost-style TTP classifier training, load, save, predict, and probability interfaces.
- `src/predictor/next_step_predictor.py` with LSTM model support and model persistence.
- `training/` scripts for `train_behavior_model.py`, `train_ttp.py`, and `train_next_step.py`.
- `src/utils/dataset.py` dataset loader handling local paths and Google Drive URLs.
- `src/planner.py` planner agent with GROQ-aware summary and recommendation generation.
- `src/feedback.py` feedback store for analyst decisions.
- `src/predictor/decision_fusion.py` for final threat scoring.
- `src/predictor/confidence_gate.py` for automated/human/analyst gate decisions.
- `api/main.py` enhanced to persist episodes, add attack graph nodes, expose top-K MITRE matches, and store feedback.
- `scripts/build_mitre_rag.py` import path fix and MITRE index build flow.
- `dashboards/streamlit_app.py` import path fix for direct execution.
- `requirements.txt` updated with `gdown`, `pytest`, and `uvicorn[standard]`.
- `PROJECT_ANALYSIS.md`, `FINAL_ARCHITECTURE.md`, `EXECUTION_GUIDE.md`, `DATASET_GUIDE.md`, `MODEL_SUMMARY.md`, `TEST_REPORT.md`, and `CHANGELOG.md` documentation files.

### Fixed

- Resolved import mismatch for `mapao.src.*` by adding `mapao/src/__init__.py` package shim.
- Corrected project root path resolution in `src/utils/config.py`.
- Added runtime path handling in `scripts/build_mitre_rag.py` and `dashboards/streamlit_app.py`.
- Added built-in unittest suite to validate core functionality.

### Notes

- The repository now supports end-to-end API analysis with sample event data using the existing architecture.
- The dataset loader is ready for CICIDS2017 external dataset integration, but training scripts use placeholder synthetic features.
