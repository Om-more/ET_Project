from __future__ import annotations

import json
from pathlib import Path

from mapao.src.rag.indexer import MitreRagIndex, get_default_indexer


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    source_path = root / "data" / "raw" / "mitre_attack_stix.json"
    if not source_path.exists():
        raise FileNotFoundError(f"MITRE STIX source not found: {source_path}")

    with source_path.open("r", encoding="utf-8") as handle:
        mitre_payload = json.load(handle)

    indexer = get_default_indexer()
    indexer.build(mitre_payload)
    print(f"Built MITRE index at {indexer.index_path}")


if __name__ == "__main__":
    main()
