import csv
from pathlib import Path

from src.decision_support import run


ROOT = Path(__file__).parent
recommendations = run(ROOT / "data")

print("SYNTHETIC DEMONSTRATION - NOT FOR OPERATIONAL USE")
for rank, item in enumerate(recommendations, start=1):
    print(
        f"{rank}. {item['team_id']} -> {item['zone_id']} | "
        f"priority={item['priority']:.3f} | "
        f"travel={item['travel_minutes']:.1f} min"
    )
    print(f"   route: {item['route']}")

output_dir = ROOT / "outputs"
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "recommendations.csv"
with output_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=recommendations[0].keys())
    writer.writeheader()
    writer.writerows(recommendations)

print(f"Saved: {output_path.relative_to(ROOT)}")
