from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


class PolicyConfig(BaseModel):
    risk: dict[str, Any]
    assets: dict[str, Any]
    audit: dict[str, Any]


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_policy_config() -> PolicyConfig:
    root = get_project_root()
    config_path = root / "configs" / "policies.yaml"
    config_data = load_yaml(config_path)
    return PolicyConfig(**config_data)
