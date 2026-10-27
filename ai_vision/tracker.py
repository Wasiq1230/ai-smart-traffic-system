"""
Multi-Object Tracker using IoU association and trajectory analysis.
"""

import time
import math
from typing import List, Dict, Any, Tuple, Optional
from ai_vision.utils import calculate_iou, estimate_speed_kmh


class TrackedObject:
    def __init__(self, track_id: int, cls_id: int, label: str, bbox: List[float], conf: float, timestamp: float):
        self.track_id = track_id
        self.cls_id = cls_id
        self.label = label
        self.bbox = bbox
        self.conf = conf
        self.cx = int((bbox[0] + bbox[2]) / 2)
        self.cy = int((bbox[1] + bbox[3]) / 2)
        self.first_seen = timestamp
        self.last_seen = timestamp
        self.positions: List[Tuple[Tuple[int, int], float]] = [((self.cx, self.cy), timestamp)]
        self.lane = "Unknown"
        self.speed_kmh = 42.0
        self.stopped_duration = 0.0
        self.is_stopped = False
        self.direction = "Southbound"
        self.hits = 1
        self.lost_frames = 0

    def update(self, bbox: List[float], conf: float, timestamp: float, pixels_per_meter: float = 8.0):
        self.bbox = bbox
        self.conf = conf
        new_cx = int((bbox[0] + bbox[2]) / 2)
        new_cy = int((bbox[1] + bbox[3]) / 2)

        dt = timestamp - self.last_seen
        if dt > 0:
            dx = new_cx - self.cx
            dy = new_cy - self.cy
            inst_speed = estimate_speed_kmh((self.cx, self.cy), (new_cx, new_cy), dt, pixels_per_meter)
            self.speed_kmh = round(0.7 * self.speed_kmh + 0.3 * inst_speed, 1)

            if abs(dx) > abs(dy):
                self.direction = "Eastbound" if dx > 0 else "Westbound"
            else:
                self.direction = "Southbound" if dy > 0 else "Northbound"

            if inst_speed < 3.0:
                self.stopped_duration += dt
                if self.stopped_duration > 3.0:
                    self.is_stopped = True
            else:
                self.stopped_duration = max(0.0, self.stopped_duration - dt)
                self.is_stopped = False

        self.cx = new_cx
        self.cy = new_cy
        self.last_seen = timestamp
        self.positions.append(((new_cx, new_cy), timestamp))
        if len(self.positions) > 30:
            self.positions.pop(0)
        self.hits += 1
        self.lost_frames = 0

    def mark_missed(self):
        self.lost_frames += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "track_id": self.track_id,
            "label": self.label,
            "cls_id": self.cls_id,
            "bbox": [round(v, 1) for v in self.bbox],
            "confidence": round(self.conf, 2),
            "centroid": [self.cx, self.cy],
            "lane": self.lane,
            "speed_kmh": self.speed_kmh,
            "is_stopped": self.is_stopped,
            "stopped_duration": round(self.stopped_duration, 1),
            "direction": self.direction,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen
        }


class SimpleTracker:
    def __init__(self, iou_threshold: float = 0.35, max_lost_frames: int = 20):
        self.iou_threshold = iou_threshold
        self.max_lost_frames = max_lost_frames
        self.tracks: Dict[int, TrackedObject] = {}
        self.next_id = 1

    def update(self, detections: List[Dict[str, Any]], timestamp: float) -> List[TrackedObject]:
        if not detections:
            for tid, track in list(self.tracks.items()):
                track.mark_missed()
                if track.lost_frames > self.max_lost_frames:
                    del self.tracks[tid]
            return list(self.tracks.values())

        track_ids = list(self.tracks.keys())
        matched_tracks = set()
        matched_dets = set()

        if track_ids:
            for d_idx, det in enumerate(detections):
                best_iou = 0.0
                best_tid = None
                for tid in track_ids:
                    if tid in matched_tracks:
                        continue
                    iou = calculate_iou(det["bbox"], self.tracks[tid].bbox)
                    if iou > best_iou:
                        best_iou = iou
                        best_tid = tid

                if best_iou >= self.iou_threshold and best_tid is not None:
                    self.tracks[best_tid].update(det["bbox"], det["conf"], timestamp)
                    matched_tracks.add(best_tid)
                    matched_dets.add(d_idx)

        for d_idx, det in enumerate(detections):
            if d_idx not in matched_dets:
                new_track = TrackedObject(
                    track_id=self.next_id,
                    cls_id=det.get("class_id", 2),
                    label=det.get("label", "car"),
                    bbox=det["bbox"],
                    conf=det.get("conf", 0.8),
                    timestamp=timestamp
                )
                self.tracks[self.next_id] = new_track
                self.next_id += 1

        for tid in track_ids:
            if tid not in matched_tracks:
                self.tracks[tid].mark_missed()
                if self.tracks[tid].lost_frames > self.max_lost_frames:
                    del self.tracks[tid]

        return list(self.tracks.values())
