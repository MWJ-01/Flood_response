import unittest
from pathlib import Path

from src.decision_support import (
    priority_score,
    read_csv,
    run,
    shortest_route,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


class DecisionSupportTests(unittest.TestCase):
    def test_priority_is_between_zero_and_one(self):
        for zone in read_csv(DATA / "zones.csv"):
            self.assertGreaterEqual(priority_score(zone), 0)
            self.assertLessEqual(priority_score(zone), 1)

    def test_general_vehicle_avoids_deep_road(self):
        edges = read_csv(DATA / "edges.csv")
        route = shortest_route(edges, "N1", "N5", depth_limit=0.30)
        self.assertIsNotNone(route)
        self.assertLessEqual(route["maximum_depth_m"], 0.30)

    def test_each_team_and_zone_is_used_once(self):
        recommendations = run(DATA)
        teams = [item["team_id"] for item in recommendations]
        zones = [item["zone_id"] for item in recommendations]
        self.assertEqual(len(teams), len(set(teams)))
        self.assertEqual(len(zones), len(set(zones)))

    def test_demo_produces_two_recommendations(self):
        recommendations = run(DATA)
        self.assertEqual(len(recommendations), 2)
        self.assertEqual(recommendations[0]["zone_id"], "ZONE-1")


if __name__ == "__main__":
    unittest.main()
