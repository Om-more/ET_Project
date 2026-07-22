# MODEL_SUMMARY

## Behavior Model

- Type: Isolation Forest
- Path: `models/isolation_forest.pkl`
- Interface:
  - `train(X)`
  - `predict(X)`
  - `save(path)`
  - `load(path)`
- Purpose: Detect anomalous behavior patterns from normalized feature vectors.

## TTP Classifier

- Type: GradientBoostingClassifier
- Path: `models/ttp_classifier.pkl`
- Interface:
  - `train(X, y)`
  - `predict(X)`
  - `predict_proba(X)`
  - `save(path)`
  - `load(path)`
- Purpose: Classify episodes into known ATT&CK technique categories.

## Next-Step Predictor

- Type: LSTM sequence classifier
- Path: `models/next_step_model.pt`
- Interface:
  - `train(X, y)`
  - `predict(X)`
  - `save(path)`
  - `load(path)`
- Purpose: Predict the next likely adversary technique or action.

## RAG Index

- Type: FAISS vector index with Sentence Transformers embeddings
- Path: `data/processed/mitre_index.faiss`
- Metadata: `data/processed/mitre_metadata.pkl`
- Purpose: Retrieve probable MITRE ATT&CK techniques from episode narrative.
