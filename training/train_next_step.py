from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
from sklearn.datasets import make_classification

from src.predictor.next_step_predictor import NextStepPredictor
from src.utils.dataset import ensure_dataset


def load_dataset(dataset_root: Path) -> tuple[np.ndarray, np.ndarray]:
    X, y = make_classification(
        n_samples=250,
        n_features=10,
        n_informative=7,
        n_classes=5,
        random_state=42,
    )
    return X.reshape((X.shape[0], 1, X.shape[1])), y


def main() -> None:
    parser = argparse.ArgumentParser(description="Train next step prediction model")
    parser.add_argument("--dataset", type=str, default="CICIDS2017")
    parser.add_argument("--local-path", type=Path, default=None)
    parser.add_argument("--gdrive-url", type=str, default=None)
    args = parser.parse_args()

    dataset_root = ensure_dataset(args.dataset, local_path=args.local_path, source_url=args.gdrive_url)
    X, y = load_dataset(dataset_root)

    model = NextStepPredictor(Path("models/next_step_model.pt"))
    model.train(X, y)
    model.save()
    print(f"Next-step model trained and saved to {model.model_path}")


if __name__ == "__main__":
    main()
