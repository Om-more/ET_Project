# EXECUTION_GUIDE

## Prerequisites

Install dependencies:

```bash
cd /workspaces/ET_Project
python -m pip install -r requirements.txt
```

## Build MITRE RAG Index

```bash
cd /workspaces/ET_Project
python scripts/build_mitre_rag.py
```

This creates `data/processed/mitre_index.faiss` and `data/processed/mitre_metadata.pkl`.

## Train Models

### Behavior model

```bash
cd /workspaces/ET_Project
python training/train_behavior_model.py --local-path data/raw
```

### TTP classifier

```bash
cd /workspaces/ET_Project
python training/train_ttp.py --local-path data/raw
```

### Next-step predictor

```bash
cd /workspaces/ET_Project
python training/train_next_step.py --local-path data/raw
```

Model artifacts are saved to:

- `models/isolation_forest.pkl`
- `models/ttp_classifier.pkl`
- `models/next_step_model.pt`

## Run API

```bash
cd /workspaces/ET_Project
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Then visit `http://localhost:8000/health`.

## Run Dashboard

```bash
cd /workspaces/ET_Project
streamlit run dashboards/streamlit_app.py
```

## Validation

Run syntax validation:

```bash
cd /workspaces/ET_Project
python -m py_compile $(find . -name '*.py')
```

Run unit tests:

```bash
cd /workspaces/ET_Project
python -m unittest tests/test_unittest_suite.py
```
