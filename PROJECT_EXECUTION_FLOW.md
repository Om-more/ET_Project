# MAPAO Project Execution Flow

## 1. Actual project entry points

The repository appears to have three practical entry points:

- API entry point: [api/main.py](api/main.py)
  - Starts a FastAPI application and exposes the `/health` and `/analyze` routes.
- Dashboard entry point: [dashboards/streamlit_app.py](dashboards/streamlit_app.py)
  - Starts the Streamlit UI for loading events, building episodes, and showing risk reasoning.
- Build script entry point: [scripts/build_mitre_rag.py](scripts/build_mitre_rag.py)
  - Builds the MITRE vector index from the raw STIX data.

## 2. Execution order

The intended runtime flow is:

1. Load configuration from [configs/policies.yaml](configs/policies.yaml).
2. Load raw event input from [data/raw/sample_events.json](data/raw/sample_events.json).
3. Parse events through [src/normalization/parser.py](src/normalization/parser.py).
4. Group normalized events into episodes in [src/episode_builder/builder.py](src/episode_builder/builder.py).
5. Build episode summaries.
6. Match MITRE techniques using [src/ttp_mapper/mapper.py](src/ttp_mapper/mapper.py) and [src/rag/indexer.py](src/rag/indexer.py).
7. Produce a risk verdict in [src/predictor/risk.py](src/predictor/risk.py).
8. Enact the decision in [src/orchestrator/engine.py](src/orchestrator/engine.py).
9. Write audit output to the path defined by the policy config under [data/processed](data/processed).

## 3. Missing imports

The following imports are referenced but are not backed by an equivalent package/module structure in the current repository layout:

- [api/main.py](api/main.py) imports `mapao.src...` modules, but the repository package root is [mapao/__init__.py](mapao/__init__.py), and the `src` package is not nested under `mapao/src` in the filesystem. The code expects `mapao.src`, but the actual source tree is rooted at [src](src).

## 4. Broken imports

The following import patterns are likely broken or fragile in practice:

- [api/main.py](api/main.py) and [dashboards/streamlit_app.py](dashboards/streamlit_app.py) import modules using `from mapao.src...` even though the repository uses a top-level [src](src) package rather than a nested [mapao/src](mapao/src) package.
- [src/ttp_mapper/mapper.py](src/ttp_mapper/mapper.py) imports [src/rag/indexer.py](src/rag/indexer.py) via `mapao.src...`, which is the same packaging mismatch.
- The repository also depends on runtime packages such as FastAPI, Streamlit, PyYAML, Pydantic, FAISS, and sentence-transformers, which are not currently available in the active Python environment.

## 5. Syntax errors

No syntax errors were detected by compilation of the repository sources.

## 6. Missing requirements

The current environment is missing the following packages:

- fastapi
- streamlit
- pyyaml
- pydantic
- faiss-cpu
- sentence-transformers

The repository also appears to expect these dependencies based on the imports and runtime usage.

## 7. Wrong module paths

The main issue is the import prefix mismatch:

- Code uses `mapao.src...`
- Actual package path in the repository is `src...`

This is the clearest wrong module path pattern in the repository.

## 8. Missing __init__.py files

The following package directories are present and have __init__.py files:

- [src/__init__.py](src/__init__.py)
- [src/episode_builder/__init__.py](src/episode_builder/__init__.py)
- [src/normalization/__init__.py](src/normalization/__init__.py)
- [src/rag/__init__.py](src/rag/__init__.py)
- [src/ttp_mapper/__init__.py](src/ttp_mapper/__init__.py)
- [mapao/__init__.py](mapao/__init__.py)

The repository does not currently contain an `__init__.py` file under some sibling package directories that may be intended to be importable as nested packages, but the core modules are already package-initialized.

## 9. Missing packages

The following runtime packages are missing from the current Python environment:

- fastapi
- streamlit
- pyyaml
- pydantic
- faiss-cpu
- sentence-transformers

## 10. Notes

- The raw input data exists under [data/raw](data/raw).
- The runtime output directory [data/processed](data/processed) is currently empty, so the index and audit artifacts are not yet generated.
- The build script [scripts/build_mitre_rag.py](scripts/build_mitre_rag.py) is the component that would populate the MITRE index artifacts required by [src/rag/indexer.py](src/rag/indexer.py).
