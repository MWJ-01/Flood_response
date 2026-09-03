"""Small and transparent decision-support prototype for a flood scenario."""

from __future__ import annotations

import csv
import heapq
from pathlib import Path


PRIORITY_WEIGHTS = {
    "flood_severity": 0.45,
    "vulnerability": 0.35,
    "waiting_time": 0.20,
}

VEHICLE_DEPTH_LIMITS = {
    "general": 0.30,
    "high_clearance": 0.50,
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def priority_score(zone: dict[str, str]) -> float:
    """Return a score from 0 to 1 using three understandable factors."""
    waiting = min(float(zone["waiting_minutes"]) / 90.0, 1.0)
    score = (
        PRIORITY_WEIGHTS["flood_severity"] * float(zone["flood_severity"])
        + PRIORITY_WEIGHTS["vulnerability"] * float(zone["vulnerability"])
        + PRIORITY_WEIGHTS["waiting_time"] * waiting
    )
    return round(score, 3)


def build_graph(edges: list[dict[str, str]], depth_limit: float):
    graph: dict[str, list[tuple[str, float, float]]] = {}
    for edge in edges:
        depth = float(edge["flood_depth_m"])
        if depth > depth_limit:
            continue
        start = edge["from_node"]
        end = edge["to_node"]
        minutes = float(edge["travel_minutes"])
        graph.setdefault(start, []).append((end, minutes, depth))
        graph.setdefault(end, []).append((start, minutes, depth))
    return graph


def shortest_route(edges, start: str, target: str, depth_limit: float):
    """Dijkstra search after roads above the vehicle limit are removed."""
    graph = build_graph(edges, depth_limit)
    queue = [(0.0, start, [start], 0.0)]
    best_time = {start: 0.0}

    while queue:
        time, node, route, maximum_depth = heapq.heappop(queue)
        if node == target:
            return {
                "travel_minutes": time,
                "route": route,
                "maximum_depth_m": maximum_depth,
            }
        if time > best_time.get(node, float("inf")):
            continue
        for next_node, edge_time, edge_depth in graph.get(node, []):
            new_time = time + edge_time
            if new_time < best_time.get(next_node, float("inf")):
                best_time[next_node] = new_time
                heapq.heappush(
                    queue,
                    (
                        new_time,
                        next_node,
                        route + [next_node],
                        max(maximum_depth, edge_depth),
                    ),
                )
    return None


def make_recommendations(edges, teams, zones):
    """Rank feasible pairs, then assign each team and zone at most once."""
    candidates = []
    for team in teams:
        if team["status"] != "available":
            continue
        depth_limit = VEHICLE_DEPTH_LIMITS[team["vehicle_type"]]
        for zone in zones:
            route = shortest_route(
                edges,
                team["start_node"],
                zone["target_node"],
                depth_limit,
            )
            if route is None:
                continue
            priority = priority_score(zone)
            action_score = priority - 0.01 * route["travel_minutes"]
            candidates.append((action_score, team, zone, priority, route))

    recommendations = []
    used_teams = set()
    used_zones = set()
    for _, team, zone, priority, route in sorted(candidates, reverse=True, key=lambda x: x[0]):
        if team["team_id"] in used_teams or zone["zone_id"] in used_zones:
            continue
        used_teams.add(team["team_id"])
        used_zones.add(zone["zone_id"])
        recommendations.append(
            {
                "team_id": team["team_id"],
                "zone_id": zone["zone_id"],
                "priority": priority,
                "travel_minutes": route["travel_minutes"],
                "maximum_depth_m": route["maximum_depth_m"],
                "route": " -> ".join(route["route"]),
            }
        )
    return recommendations


def run(data_dir: Path):
    edges = read_csv(data_dir / "edges.csv")
    teams = read_csv(data_dir / "teams.csv")
    zones = read_csv(data_dir / "zones.csv")
    return make_recommendations(edges, teams, zones)
