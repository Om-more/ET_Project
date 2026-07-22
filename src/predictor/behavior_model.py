from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class BehaviorModel:
    def __init__(self, model_path: Path | None = None) -> None:
        self.model_path = model_path or Path("models/isolation_forest.pkl")
        self.scaler_path = self.model_path.with_name("behavior_scaler.pkl")
        self.model: IsolationForest | None = None
        self.scaler: StandardScaler | None = None

    def train(self, X: np.ndarray, y: np.ndarray | None = None) -> None:
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        self.model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        self.model.fit(X_scaled)

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.model is None or self.scaler is None:
            raise ValueError("Model not loaded")
        X_scaled = self.scaler.transform(X)
        scores = self.model.decision_function(X_scaled)
        return -scores

    def save(self, path: Path | None = None) -> None:
        path = path or self.model_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if self.model is None or self.scaler is None:
            raise ValueError("No trained model to save")
        with path.open("wb") as handle:
            pickle.dump({"model": self.model}, handle)
        with self.scaler_path.open("wb") as handle:
            pickle.dump(self.scaler, handle)

    def load(self, path: Path | None = None) -> None:
        path = path or self.model_path
        if not path.exists() or not self.scaler_path.exists():
            raise FileNotFoundError("Behavior model files not found")
        with path.open("rb") as handle:
            state = pickle.load(handle)
        self.model = state["model"]
        with self.scaler_path.open("rb") as handle:
            self.scaler = pickle.load(handle)
