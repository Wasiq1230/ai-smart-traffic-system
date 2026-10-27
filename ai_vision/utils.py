"""
Geometry, image transformation and computer vision utility functions.
"""

import math
from typing import List, Tuple, Dict, Any, Optional

def is_point_in_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
    """Ray casting algorithm to determine if a 2D point is inside a polygon."""
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def calculate_iou(boxA: List[float], boxB: List[float]) -> float:
    """Calculate Intersection over Union (IoU) of two bounding boxes [x1, y1, x2, y2]."""
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0.0, xB - xA) * max(0.0, yB - yA)
    boxAArea = max(0.0, boxA[2] - boxA[0]) * max(0.0, boxA[3] - boxA[1])
    boxBArea = max(0.0, boxB[2] - boxB[0]) * max(0.0, boxB[3] - boxB[1])

    denom = float(boxAArea + boxBArea - interArea)
    if denom <= 0:
        return 0.0
    return interArea / denom

def estimate_speed_kmh(pos1: Tuple[int, int], pos2: Tuple[int, int], dt_seconds: float, pixels_per_meter: float = 8.0) -> float:
    """Estimate speed in km/h based on pixel movement over time interval dt."""
    if dt_seconds <= 0:
        return 0.0
    pixel_dist = math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)
    meters = pixel_dist / max(0.1, pixels_per_meter)
    speed_mps = meters / dt_seconds
    speed_kmh = speed_mps * 3.6
    return round(min(160.0, max(0.0, speed_kmh)), 1)
