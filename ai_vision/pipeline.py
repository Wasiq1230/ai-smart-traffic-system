"""
Unified AI Vision Pipeline.
"""

import time
from typing import Dict, Any, Optional, List
import numpy as np

from ai_vision.video_processor import VideoProcessor
from ai_vision.model_loader import ModelLoader
from ai_vision.yolo_detector import YOLODetector
from ai_vision.tracker import SimpleTracker
from ai_vision.lane_detector import LaneDetector
from ai_vision.vehicle_counter import VehicleCounter
from ai_vision.emergency_detector import EmergencyDetector
from ai_vision.accident_detector import AccidentDetector
from ai_vision.violation_detector import ViolationDetector
from ai_vision.multimodal_detector import MultimodalDetector
from ai_vision.anpr import ANPRSystem
from ai_vision.logger import get_logger

logger = get_logger("VisionPipeline")


class VisionPipeline:
    def __init__(
        self,
        video_source: str = "0",
        intersection_id: str = "INT-001",
        conf_thresh: float = 0.35
    ):
        self.intersection_id = intersection_id
        self.video_processor = VideoProcessor(source=video_source, loop=True)
        self.model_loader = ModelLoader()
        self.detector = YOLODetector(model_loader=self.model_loader, conf_thresh=conf_thresh)
        self.tracker = SimpleTracker()
        self.lane_detector = LaneDetector()
        self.counter = VehicleCounter()
        self.emergency_detector = EmergencyDetector()
        self.accident_detector = AccidentDetector()
        self.violation_detector = ViolationDetector()
        self.multimodal_detector = MultimodalDetector()
        self.anpr_system = ANPRSystem()

    def process_next_frame(self, signal_states: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        ok, frame, meta = self.video_processor.get_frame()
        if not ok or frame is None:
            return None

        return self.process_frame(frame, meta, signal_states)

    def process_frame(
        self,
        frame: np.ndarray,
        metadata: Dict[str, Any],
        signal_states: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        t0 = time.time()
        timestamp = metadata.get("timestamp", t0)
        frame_idx = metadata.get("frame_idx", 0)

        raw_detections = self.detector.detect(frame)
        tracked_objects = self.tracker.update(raw_detections, timestamp)
        lane_results = self.lane_detector.assign_lanes(tracked_objects)
        count_summary = self.counter.update(tracked_objects)
        emergency_alerts = self.emergency_detector.analyze(frame, tracked_objects)
        accidents = self.accident_detector.detect(tracked_objects)
        violations = self.violation_detector.check_violations(tracked_objects, signal_states)
        multimodal = self.multimodal_detector.analyze(tracked_objects)
        anpr_records = self.anpr_system.process_frame(frame, tracked_objects)

        inference_time_ms = round((time.time() - t0) * 1000, 2)

        traffic_intelligence = {
            "intersection_id": self.intersection_id,
            "frame_idx": frame_idx,
            "timestamp": timestamp,
            "inference_time_ms": inference_time_ms,
            "active_vehicle_count": count_summary["active_vehicle_count"],
            "total_unique_count": count_summary["total_unique_count"],
            "vehicle_breakdown": count_summary["active_by_type"],
            "lane_analytics": lane_results["lanes"],
            "tracked_vehicles": [obj.to_dict() for obj in tracked_objects],
            "emergency_alerts": emergency_alerts,
            "accidents": accidents,
            "violations": violations,
            "multimodal": multimodal,
            "anpr_records": anpr_records,
            "system_health": {
                "vision_fps": round(1000.0 / max(1.0, inference_time_ms), 1),
                "model_backend": self.model_loader.backend,
                "status": "HEALTHY"
            }
        }

        return traffic_intelligence
