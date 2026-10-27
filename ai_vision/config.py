"""
Configuration settings for AI Vision module.
"""

import os
from typing import Dict, List, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")

DEFAULT_YOLO_MODEL = os.path.join(MODELS_DIR, "yolov8n.pt")
FALLBACK_YOLO_MODEL = "yolov8n.pt"

DEFAULT_FRAME_WIDTH = 640
DEFAULT_FRAME_HEIGHT = 480
DEFAULT_TARGET_FPS = 15

CONFIDENCE_THRESHOLD = 0.35
IOU_THRESHOLD = 0.45
TRACK_MAX_AGE = 30
TRACK_MIN_HITS = 2

VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
    0: "pedestrian",
    1: "bicycle"
}

DEFAULT_LANE_POLYGONS: Dict[str, List[Tuple[int, int]]] = {
    "Northbound": [(220, 0), (320, 0), (320, 480), (220, 480)],
    "Southbound": [(320, 0), (420, 0), (420, 480), (320, 480)],
    "Eastbound":  [(0, 180), (640, 180), (640, 280), (0, 280)],
    "Westbound":  [(0, 280), (640, 280), (640, 380), (0, 380)]
}

EMERGENCY_CLASSES = ["ambulance", "fire truck", "police", "emergency"]
