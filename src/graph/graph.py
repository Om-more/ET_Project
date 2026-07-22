from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import networkx as nx

from src.episode_builder.models import Episode
from src.normalization.models import NormalizedEvent
from src.ttp_mapper.mapper import TtpMatch


@dataclass
class GraphNode:
    identifier: str
    node_type: str
    properties: dict[str, Any]


class AttackGraph:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_episode(self, episode: Episode) -> None:
        self.graph.add_node(
            episode.episode_id,
            type="episode",
            entity_key=episode.entity_key,
            start_time=episode.start_time,
            end_time=episode.end_time,
            event_count=episode.event_count,
        )
        for event in episode.events:
            self.add_event(event)
            self.graph.add_edge(episode.episode_id, event.event_id, relationship="contains")

    def add_event(self, event: NormalizedEvent) -> None:
        self.graph.add_node(
            event.event_id,
            type="event",
            timestamp=event.timestamp.isoformat(),
            telemetry_type=event.telemetry_type,
            activity=event.activity.action,
        )

        source = event.source_entity
        if source.host_id:
            self._add_entity_node(source.host_id, "host")
            self.graph.add_edge(event.event_id, source.host_id, relationship="originates_from")
        if source.user_id:
            self._add_entity_node(source.user_id, "user")
            self.graph.add_edge(event.event_id, source.user_id, relationship="initiated_by")
        if source.ip:
            self._add_entity_node(source.ip, "ip")
            self.graph.add_edge(event.event_id, source.ip, relationship="uses_ip")

        if event.destination_entity:
            dest = event.destination_entity
            if dest.host_id:
                self._add_entity_node(dest.host_id, "host")
                self.graph.add_edge(event.event_id, dest.host_id, relationship="targets")
            if dest.ip:
                self._add_entity_node(dest.ip, "ip")
                self.graph.add_edge(event.event_id, dest.ip, relationship="targets")

        if event.activity.process_name:
            self._add_entity_node(event.activity.process_name, "process")
            self.graph.add_edge(event.event_id, event.activity.process_name, relationship="executes")
            if event.activity.parent_process:
                self._add_entity_node(event.activity.parent_process, "process")
                self.graph.add_edge(event.activity.process_name, event.activity.parent_process, relationship="spawned_by")

    def add_technique(self, technique: TtpMatch, episode_id: str | None = None) -> None:
        self.graph.add_node(
            technique.matched_ttp_id,
            type="technique",
            name=technique.matched_ttp_name,
            description=technique.description,
            confidence=technique.ttp_confidence,
        )
        if episode_id and self.graph.has_node(episode_id):
            self.graph.add_edge(episode_id, technique.matched_ttp_id, relationship="indicates")

    def _add_entity_node(self, identifier: str, entity_type: str) -> None:
        if self.graph.has_node(identifier):
            existing = self.graph.nodes[identifier]
            if existing.get("type") != entity_type:
                existing["type"] = entity_type
            return
        self.graph.add_node(identifier, type=entity_type)

    def get_neighbors(self, node_id: str) -> list[str]:
        if not self.graph.has_node(node_id):
            return []
        return list(self.graph.successors(node_id)) + list(self.graph.predecessors(node_id))

    def find_shortest_path(self, source: str, target: str) -> list[str] | None:
        try:
            return nx.shortest_path(self.graph, source, target)
        except nx.NetworkXNoPath:
            return None
        except nx.NodeNotFound:
            return None

    def query_nodes_by_type(self, node_type: str) -> list[str]:
        return [node for node, details in self.graph.nodes(data=True) if details.get("type") == node_type]

    def serialize(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        nx.write_gpickle(self.graph, path)

    def deserialize(self, path: Path) -> None:
        if not path.exists():
            raise FileNotFoundError(f"Graph file not found: {path}")
        self.graph = nx.read_gpickle(path)
