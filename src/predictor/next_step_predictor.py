from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn as nn


class _NextStepLstm(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int) -> None:
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        _, (hidden, _) = self.lstm(x)
        return self.fc(hidden[-1])


class NextStepPredictor:
    def __init__(self, model_path: Path | None = None) -> None:
        self.model_path = model_path or Path("models/next_step_model.pt")
        self.model: _NextStepLstm | None = None
        self.input_size = 10
        self.hidden_size = 32
        self.output_size = 5

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        model = _NextStepLstm(self.input_size, self.hidden_size, self.output_size)
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.long)

        model.train()
        for _epoch in range(10):
            optimizer.zero_grad()
            logits = model(X_tensor)
            loss = criterion(logits, y_tensor)
            loss.backward()
            optimizer.step()

        self.model = model

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model not loaded")
        self.model.eval()
        X_tensor = torch.tensor(X, dtype=torch.float32)
        with torch.no_grad():
            logits = self.model(X_tensor)
        return logits.argmax(dim=-1).numpy()

    def save(self, path: Path | None = None) -> None:
        path = path or self.model_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if self.model is None:
            raise ValueError("No trained model to save")
        torch.save(self.model.state_dict(), path)

    def load(self, path: Path | None = None) -> None:
        path = path or self.model_path
        if not path.exists():
            raise FileNotFoundError("Next step model file not found")
        model = _NextStepLstm(self.input_size, self.hidden_size, self.output_size)
        model.load_state_dict(torch.load(path))
        model.eval()
        self.model = model
