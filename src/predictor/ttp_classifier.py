from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier


class TtpClassifier:
    def __init__(self, model_path: Path | None = None) -> None:
        self.model_path = model_path or Path("models/ttp_classifier.pkl")
        self.model: GradientBoostingClassifier | None = None

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        self.model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model not loaded")
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model not loaded")
        return self.model.predict_proba(X)

    def save(self, path: Path | None = None) -> None:
        path = path or self.model_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if self.model is None:
            raise ValueError("No trained model to save")
        with path.open("wb") as handle:
            pickle.dump(self.model, handle)

    def load(self, path: Path | None = None) -> None:
        path = path or self.model_path
        if not path.exists():
            raise FileNotFoundError("TTP classifier model not found")
        with path.open("rb") as handle:
            self.model = pickle.load(handle)
