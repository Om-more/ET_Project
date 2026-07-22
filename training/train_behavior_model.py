from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
from sklearn.datasets import make_blobs

from src.predictor.behavior_model import BehaviorModel
from src.utils.dataset import ensure_dataset


def load_dataset(dataset_root: Path) -> np.ndarray:
    # Placeholder synthetic loader; replace with real CICIDS2017 feature extraction.
    X, _ = make_blobs(n_samples=200, centers=3, n_features=10, random_state=42)
    return X


def main() -> None:
    parser = argparse.ArgumentParser(description="Train behavior anomaly model")
    parser.add_argument("--dataset", type=str, default="CICIDS2017")
    parser.add_argument("--local-path", type=Path, default=None)
    parser.add_argument("--gdrive-url", type=str, default=None)
    args = parser.parse_args()

    dataset_root = ensure_dataset(args.dataset, local_path=args.local_path, source_url=args.gdrive_url)
    X = load_dataset(dataset_root)

    model = BehaviorModel(Path("models/isolation_forest.pkl"))
    model.train(X)
    model.save()
    print(f"Behavior model trained and saved to {model.model_path}")


if __name__ == "__main__":
    main()
