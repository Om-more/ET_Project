from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any

from src.utils.config import get_project_root

try:
    import faiss
except ModuleNotFoundError:  # pragma: no cover - import guard for minimal environments
    faiss = None


class MitreRagIndex:
    def __init__(self, index_path: Path, metadata_path: Path, model_name: str = "all-MiniLM-L6-v2"):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.model = self._load_model(model_name)
        self.index: Any | None = None
        self.metadata: list[dict[str, Any]] = []

    def _load_model(self, model_name: str) -> Any:
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer(model_name)

    def build(self, mitre_data: dict[str, Any]) -> None:
        attack_patterns = []
        embeddings = []

        for item in mitre_data.get("objects", []):
            if item.get("type") != "attack-pattern":
                continue
            description = item.get("description", "")
            name = item.get("name", "")
            external_references = item.get("external_references", [])
            technique_id = next(
                (ref.get("external_id") for ref in external_references if ref.get("source_name") == "mitre-attack"),
                None,
            )
            if not technique_id:
                continue

            text = f"{technique_id}: {name}. {description}"
            attack_patterns.append({
                "id": technique_id,
                "name": name,
                "description": description,
                "text": text,
            })

        if not attack_patterns:
            raise ValueError("No attack-patterns found in MITRE data")

        corpus = [entry["text"] for entry in attack_patterns]
        if faiss is None:
            raise ImportError("faiss is required to build the MITRE index")

        embeddings = self.model.encode(corpus, normalize_embeddings=True)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)
        self.metadata = attack_patterns

        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
        with self.metadata_path.open("wb") as handle:
            pickle.dump(self.metadata, handle)

    def load(self) -> None:
        if faiss is None:
            raise ImportError("faiss is required to load the MITRE index")

        self.index = faiss.read_index(str(self.index_path))
        with self.metadata_path.open("rb") as handle:
            self.metadata = pickle.load(handle)

    def retrieve_top_k(self, query_text: str, k: int = 3) -> list[dict[str, Any]]:
        if self.index is None:
            self.load()

        query_embedding = self.model.encode([query_text], normalize_embeddings=True)
        distances, indices = self.index.search(query_embedding, k)
        results = []
        for score, idx in zip(distances[0], indices[0]):
            if idx < 0:
                continue
            meta = self.metadata[idx].copy()
            meta["score"] = float(score)
            results.append(meta)

        return results


def get_default_indexer() -> MitreRagIndex:
    root = get_project_root()
    index_path = root / "data" / "processed" / "mitre_index.faiss"
    metadata_path = root / "data" / "processed" / "mitre_metadata.pkl"
    return MitreRagIndex(index_path=index_path, metadata_path=metadata_path)
