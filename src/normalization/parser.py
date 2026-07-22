from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.normalization.models import ActivityContext, EntityContext, NormalizedEvent


def parse_raw_event(raw: dict[str, Any], raw_ref: str) -> NormalizedEvent:
    if not isinstance(raw, dict):
        raise TypeError(f"Expected event object as dict in {raw_ref}, got {type(raw).__name__}")

    source = raw.get("source") or {}
    dest = raw.get("destination") or {}
    activity = raw.get("activity") or {}

    if not isinstance(source, dict):
        raise TypeError(f"Expected 'source' object to be a dict in {raw_ref}")
    if not isinstance(dest, dict):
        raise TypeError(f"Expected 'destination' object to be a dict in {raw_ref}")
    if not isinstance(activity, dict):
        raise TypeError(f"Expected 'activity' object to be a dict in {raw_ref}")

    source_entity = EntityContext(
        ip=source.get("ip"),
        host_id=source.get("host_id"),
        user_id=source.get("user_id"),
    )
    destination_entity = EntityContext(
        ip=dest.get("ip"),
        host_id=dest.get("host_id"),
        user_id=dest.get("user_id"),
    ) if dest else None

    activity_context = ActivityContext(
        action=activity.get("action", "unknown"),
        process_name=activity.get("process_name"),
        cmd_line=activity.get("cmd_line"),
        parent_process=activity.get("parent_process"),
    )

    try:
        return NormalizedEvent(
            event_id=raw.get("event_id", raw.get("id", "unknown-event")),
            timestamp=_parse_timestamp(raw.get("timestamp")),
            telemetry_type=raw.get("telemetry_type", "endpoint"),
            source_entity=source_entity,
            destination_entity=destination_entity,
            activity=activity_context,
            raw_log_ref=raw_ref,
            metadata=raw.get("metadata"),
        )
    except ValidationError as exc:
        raise ValueError(f"Invalid event payload for {raw_ref}: {exc}") from exc


def _parse_timestamp(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = f"{text[:-1]}+00:00"
        try:
            return datetime.fromisoformat(text)
        except ValueError as exc:
            raise ValueError(f"Invalid timestamp value: {value}") from exc
    raise ValueError(f"Invalid timestamp value: {value}")


def load_json_events(path: Path) -> list[NormalizedEvent]:
    import json

    if not path.exists():
        raise FileNotFoundError(f"Event file not found: {path}")

    try:
        with path.open("r", encoding="utf-8") as handle:
            raw_items = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc

    if isinstance(raw_items, dict):
        raw_items = [raw_items]
    elif not isinstance(raw_items, list):
        raise ValueError(f"Expected JSON array or object in {path}, got {type(raw_items).__name__}")

    parsed_events: list[NormalizedEvent] = []
    for index, item in enumerate(raw_items):
        if not isinstance(item, dict):
            raise TypeError(f"Expected event object at index {index} in {path}, got {type(item).__name__}")
        parsed_events.append(parse_raw_event(item, str(path)))

    return parsed_events
