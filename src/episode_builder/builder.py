from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.episode_builder.models import Episode
from src.normalization.models import NormalizedEvent


def group_events_into_episodes(events: Iterable[NormalizedEvent], window_minutes: int = 10) -> list[Episode]:
    sorted_events = sorted(events, key=lambda item: item.timestamp)
    episodes: list[Episode] = []
    current_episode: list[NormalizedEvent] = []
    current_key: str | None = None
    window = timedelta(minutes=window_minutes)

    def event_key(event: NormalizedEvent) -> str:
        metadata = event.metadata or {}
        session_id = next(
            (
                str(metadata[key])
                for key in ("session_id", "session", "sessionid", "trace_id", "correlation_id")
                if metadata.get(key)
            ),
            None,
        )
        source = event.source_entity
        destination = event.destination_entity
        values = [
            ("user", source.user_id or (destination.user_id if destination else None)),
            ("host", source.host_id or (destination.host_id if destination else None)),
            ("session", session_id),
            ("ip", source.ip or (destination.ip if destination else None)),
        ]
        present = [f"{name}:{value}" for name, value in values if value not in (None, "")]
        if present:
            return "|".join(present)
        return f"process:{event.activity.process_name or event.activity.parent_process or 'unknown'}"

    def related_events(previous: NormalizedEvent, current: NormalizedEvent) -> bool:
        time_gap = current.timestamp - previous.timestamp
        if time_gap > window:
            return False

        previous_context = event_key(previous)
        current_context = event_key(current)
        if previous_context == current_context:
            return True

        metadata = current.metadata or {}
        session_id = next(
            (
                str(metadata[key])
                for key in ("session_id", "session", "sessionid", "trace_id", "correlation_id")
                if metadata.get(key)
            ),
            None,
        )
        previous_values = {
            "user": previous.source_entity.user_id or (previous.destination_entity.user_id if previous.destination_entity else None),
            "host": previous.source_entity.host_id or (previous.destination_entity.host_id if previous.destination_entity else None),
            "session": next(
                (
                    str((previous.metadata or {}).get(key))
                    for key in ("session_id", "session", "sessionid", "trace_id", "correlation_id")
                    if (previous.metadata or {}).get(key)
                ),
                None,
            ),
            "ip": previous.source_entity.ip or (previous.destination_entity.ip if previous.destination_entity else None),
        }
        current_values = {
            "user": current.source_entity.user_id or (current.destination_entity.user_id if current.destination_entity else None),
            "host": current.source_entity.host_id or (current.destination_entity.host_id if current.destination_entity else None),
            "session": session_id,
            "ip": current.source_entity.ip or (current.destination_entity.ip if current.destination_entity else None),
        }

        for field in ("user", "host", "session", "ip"):
            prev_value = previous_values[field]
            curr_value = current_values[field]
            if prev_value and curr_value and prev_value == curr_value:
                return True

        previous_process_chain = [
            value
            for value in (previous.activity.process_name, previous.activity.parent_process)
            if value
        ]
        current_process_chain = [
            value
            for value in (current.activity.process_name, current.activity.parent_process)
            if value
        ]
        if previous_process_chain and current_process_chain:
            if previous_process_chain[-1] == current_process_chain[0]:
                return True
            if set(previous_process_chain).intersection(current_process_chain):
                return True

        return False

    def flush_episode(events_block: list[NormalizedEvent], key: str) -> None:
        if not events_block:
            return
        episodes.append(
            Episode(
                episode_id=f"episode-{len(episodes)+1}",
                start_time=events_block[0].timestamp.isoformat(),
                end_time=events_block[-1].timestamp.isoformat(),
                entity_key=key,
                events=events_block.copy(),
                event_count=len(events_block),
            )
        )

    for event in sorted_events:
        key = event_key(event)
        if current_episode and (not related_events(current_episode[-1], event) or event.timestamp - current_episode[-1].timestamp > window):
            flush_episode(current_episode, current_key or "unknown")
            current_episode = []
        current_episode.append(event)
        current_key = key

    if current_episode:
        flush_episode(current_episode, current_key or "unknown")

    return episodes


def build_episode_summary(episode: Episode) -> str:
    narrative_lines = []
    for event in episode.events:
        activity = event.activity
        narrative_lines.append(
            f"[{event.timestamp.isoformat()}] {activity.action} on {event.source_entity.host_id or event.source_entity.user_id or event.source_entity.ip}"
        )
        if activity.process_name:
            narrative_lines.append(f"    process={activity.process_name}")
        if activity.cmd_line:
            narrative_lines.append(f"    cmd={activity.cmd_line}")
        if activity.parent_process:
            narrative_lines.append(f"    parent={activity.parent_process}")

    return "\n".join(narrative_lines)
