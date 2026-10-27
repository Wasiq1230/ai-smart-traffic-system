import csv
import math
import random
from datetime import datetime, timedelta

def generate_synthetic_history(output_path: str, days: int = 7):
    start_time = datetime.now() - timedelta(days=days)
    records = []
    total_steps = days * 24 * 12

    for step in range(total_steps):
        t = start_time + timedelta(minutes=5 * step)
        hour = t.hour + t.minute / 60.0
        morning_peak = 35.0 * math.exp(-((hour - 8.5) ** 2) / 2.0)
        evening_peak = 45.0 * math.exp(-((hour - 17.5) ** 2) / 3.0)
        base = 15.0 + morning_peak + evening_peak + random.gauss(0, 3.0)
        volume = max(5, int(base))

        records.append({
            "timestamp": t.isoformat(),
            "intersection_id": "INT-001",
            "vehicle_count": volume,
            "density": round(min(1.0, volume / 80.0), 3),
            "avg_speed_kmh": round(max(15.0, 50.0 - (volume / 2.0)), 1)
        })

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "intersection_id", "vehicle_count", "density", "avg_speed_kmh"])
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated {len(records)} synthetic historical records to {output_path}")
