import pytest
import numpy as np
from ai_vision.video_processor import VideoProcessor
from ai_vision.model_loader import ModelLoader
from ai_vision.yolo_detector import YOLODetector
from ai_vision.tracker import SimpleTracker, TrackedObject
from ai_vision.lane_detector import LaneDetector
from ai_vision.vehicle_counter import VehicleCounter
from ai_vision.emergency_detector import EmergencyDetector
from ai_vision.accident_detector import AccidentDetector
from ai_vision.violation_detector import ViolationDetector
from ai_vision.pipeline import VisionPipeline

def test_video_processor_fallback():
    vp = VideoProcessor(source="invalid_source.mp4")
    ok, frame, meta = vp.get_frame()
    assert ok is True
    assert frame is not None
    assert frame.shape == (480, 640, 3)
    assert meta["source"] == "simulated_fallback"

def test_model_loader_and_detector():
    loader = ModelLoader()
    assert loader.is_loaded is True
    detector = YOLODetector(model_loader=loader)
    synthetic_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    dets = detector.detect(synthetic_frame)
    assert isinstance(dets, list)

def test_tracker_and_counter():
    tracker = SimpleTracker()
    counter = VehicleCounter()
    
    dets = [
        {"bbox": [100, 100, 200, 200], "class_id": 2, "label": "car", "conf": 0.9},
        {"bbox": [300, 200, 400, 300], "class_id": 5, "label": "bus", "conf": 0.85}
    ]
    tracks = tracker.update(dets, timestamp=100.0)
    assert len(tracks) == 2
    
    summary = counter.update(tracks)
    assert summary["active_vehicle_count"] == 2
    assert summary["total_unique_count"] == 2
    assert summary["cumulative_by_type"]["car"] == 1
    assert summary["cumulative_by_type"]["bus"] == 1

def test_lane_detector():
    ld = LaneDetector()
    t = TrackedObject(track_id=1, cls_id=2, label="car", bbox=[250, 100, 300, 150], conf=0.9, timestamp=100.0)
    res = ld.assign_lanes([t])
    assert "Northbound" in res["lanes"]
    assert t.lane == "Northbound"

def test_emergency_detector():
    ed = EmergencyDetector()
    t = TrackedObject(track_id=1, cls_id=2, label="ambulance", bbox=[250, 100, 300, 150], conf=0.95, timestamp=100.0)
    t.lane = "Northbound"
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    alerts = ed.analyze(frame, [t])
    assert len(alerts) == 1
    assert alerts[0]["vehicle_type"] == "ambulance"
    assert alerts[0]["priority_status"] == "ACTIVE_PREEMPTION"

def test_accident_detector():
    ad = AccidentDetector(stop_time_threshold=2.0)
    t = TrackedObject(track_id=1, cls_id=2, label="car", bbox=[250, 100, 300, 150], conf=0.9, timestamp=100.0)
    t.is_stopped = True
    t.stopped_duration = 5.0
    t.lane = "Northbound"
    accidents = ad.detect([t])
    assert len(accidents) == 1
    assert accidents[0]["type"] == "STATIONARY_VEHICLE_OBSTRUCTION"

def test_violation_detector():
    vd = ViolationDetector(speed_limit_kmh=50.0)
    t = TrackedObject(track_id=1, cls_id=2, label="car", bbox=[250, 100, 300, 150], conf=0.9, timestamp=100.0)
    t.speed_kmh = 75.0
    t.lane = "Northbound"
    viols = vd.check_violations([t], signal_states={"Northbound": "RED"})
    assert len(viols) >= 1
    types = [v["type"] for v in viols]
    assert "SPEEDING" in types or "RED_LIGHT_RUNNING" in types

def test_full_vision_pipeline():
    pipe = VisionPipeline(video_source="invalid_source.mp4")
    res = pipe.process_next_frame()
    assert res is not None
    assert "lane_analytics" in res
    assert "tracked_vehicles" in res
    assert "system_health" in res
    assert res["system_health"]["status"] == "HEALTHY"
