from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.orchestrator.models import RiskVerdict
from src.utils.config import get_project_root, load_policy_config


def _get_audit_log_path() -> Path:
    root = get_project_root()
    policy = load_policy_config()
    return root / policy.audit["log_file"]


def _append_audit_entry(entry: dict[str, Any]) -> None:
    path = _get_audit_log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    if path.exists():
        with path.open("r", encoding="utf-8") as handle:
            try:
                existing = json.load(handle)
            except json.JSONDecodeError:
                existing = []

    existing.append(entry)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(existing, handle, indent=2)


def isolate_host(host_id: str) -> dict[str, Any]:
    result = {
        "action": "isolate_host",
        "target": host_id,
        "status": "executed",
    }
    _append_audit_entry({"type": "isolate_host", "host_id": host_id, **result})
    return result


def revoke_credentials(user_id: str) -> dict[str, Any]:
    result = {
        "action": "revoke_credentials",
        "target": user_id,
        "status": "executed",
    }
    _append_audit_entry({"type": "revoke_credentials", "user_id": user_id, **result})
    return result


def block_ip(ip_address: str) -> dict[str, Any]:
    result = {
        "action": "block_ip",
        "target": ip_address,
        "status": "executed",
    }
    _append_audit_entry({"type": "block_ip", "ip_address": ip_address, **result})
    return result


def enact_risk_verdict(verdict: RiskVerdict, entity_identifier: str | None = None) -> dict[str, Any]:
    if verdict.gate_decision != "SOAR_AUTOMATED":
        return {
            "action": "no_automation",
            "reason": verdict.gate_decision,
        }

    if verdict.recommended_action == "isolate_host" and entity_identifier:
        return isolate_host(entity_identifier)
    if verdict.recommended_action == "revoke_user_token" and entity_identifier:
        return revoke_credentials(entity_identifier)
    if verdict.recommended_action == "block_ip" and entity_identifier:
        return block_ip(entity_identifier)

    return {
        "action": "no_automation",
        "reason": "unsupported_action_or_missing_entity",
    }
