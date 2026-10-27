from typing import Dict, Any, Tuple

class CongestionAnalyzer:
    LEVELS = [
        (0.30, "LOW"),
        (0.60, "MEDIUM"),
        (0.80, "HIGH"),
        (1.00, "CRITICAL")
    ]

    def __init__(self, free_flow_speed_kmh: float = 50.0):
        self.free_flow_speed_kmh = free_flow_speed_kmh

    def evaluate_lane(self, density_score: float, avg_speed_kmh: float, queue_meters: float) -> Tuple[str, float]:
        d_comp = min(1.0, max(0.0, density_score))
        speed = max(0.0, min(self.free_flow_speed_kmh, avg_speed_kmh))
        s_comp = (self.free_flow_speed_kmh - speed) / max(1.0, self.free_flow_speed_kmh)
        q_comp = min(1.0, queue_meters / 100.0)

        composite_index = round(0.40 * d_comp + 0.35 * s_comp + 0.25 * q_comp, 3)

        level = "CRITICAL"
        for thresh, label in self.LEVELS:
            if composite_index <= thresh:
                level = label
                break

        return level, composite_index
