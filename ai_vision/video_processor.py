"""
Video Ingestion and Frame Preprocessing Processor.
"""

import os
import time
from typing import Generator, Tuple, Optional, Dict, Any
import cv2
import numpy as np

from ai_vision.logger import get_logger

logger = get_logger("VideoProcessor")


class VideoProcessor:
    def __init__(
        self,
        source: str = "0",
        target_width: int = 640,
        target_height: int = 480,
        target_fps: int = 15,
        loop: bool = False
    ):
        self.source = source
        self.target_width = target_width
        self.target_height = target_height
        self.target_fps = target_fps
        self.loop = loop
        self.cap: Optional[cv2.VideoCapture] = None
        self.total_frames = 0
        self.source_fps = 30.0
        self.frame_idx = 0
        self.is_opened = False
        self._init_source()

    def _init_source(self) -> bool:
        try:
            if str(self.source).isdigit():
                self.cap = cv2.VideoCapture(int(self.source))
            else:
                self.cap = cv2.VideoCapture(str(self.source))

            if self.cap and self.cap.isOpened():
                self.is_opened = True
                self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                self.source_fps = fps if fps > 0 else 30.0
                logger.info(f"Video opened: {self.source} ({self.total_frames} frames, {self.source_fps:.1f} FPS)")
                return True
            else:
                self.is_opened = False
                logger.warning(f"Failed to open video source: {self.source}")
                return False
        except Exception as e:
            logger.error(f"Error opening video source: {e}")
            self.is_opened = False
            return False

    def get_frame(self) -> Tuple[bool, Optional[np.ndarray], Dict[str, Any]]:
        if not self.is_opened or self.cap is None:
            return self._generate_fallback_frame()

        ret, frame = self.cap.read()
        if not ret or frame is None:
            if self.loop and self.total_frames > 0:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.frame_idx = 0
                ret, frame = self.cap.read()
            else:
                return False, None, {"frame_idx": self.frame_idx, "timestamp": time.time(), "eof": True}

        if frame is None:
            return False, None, {"frame_idx": self.frame_idx, "timestamp": time.time(), "eof": True}

        if frame.shape[1] != self.target_width or frame.shape[0] != self.target_height:
            frame = cv2.resize(frame, (self.target_width, self.target_height))

        self.frame_idx += 1
        metadata = {
            "frame_idx": self.frame_idx,
            "timestamp": time.time(),
            "source": str(self.source),
            "width": self.target_width,
            "height": self.target_height,
            "eof": False
        }
        return True, frame, metadata

    def _generate_fallback_frame(self) -> Tuple[bool, np.ndarray, Dict[str, Any]]:
        self.frame_idx += 1
        frame = np.zeros((self.target_height, self.target_width, 3), dtype=np.uint8)
        cv2.rectangle(frame, (200, 0), (440, self.target_height), (50, 50, 50), -1)
        cv2.rectangle(frame, (0, 160), (self.target_width, 320), (50, 50, 50), -1)
        cv2.line(frame, (320, 0), (320, self.target_height), (255, 255, 255), 2)
        cv2.line(frame, (0, 240), (self.target_width, 240), (255, 255, 255), 2)
        cv2.putText(frame, f"CAM-01 [SIMULATED] Frame: {self.frame_idx}", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 200), 2)
        meta = {
            "frame_idx": self.frame_idx,
            "timestamp": time.time(),
            "source": "simulated_fallback",
            "width": self.target_width,
            "height": self.target_height,
            "eof": False
        }
        return True, frame, meta

    def frame_generator(self, max_frames: Optional[int] = None) -> Generator[Tuple[int, np.ndarray, Dict[str, Any]], None, None]:
        count = 0
        frame_interval = 1.0 / max(1, self.target_fps)
        while True:
            if max_frames is not None and count >= max_frames:
                break
            start_t = time.time()
            ok, frame, meta = self.get_frame()
            if not ok or frame is None:
                if meta.get("eof"):
                    break
                continue
            yield count, frame, meta
            count += 1
            elapsed = time.time() - start_t
            sleep_t = frame_interval - elapsed
            if sleep_t > 0.001:
                time.sleep(sleep_t)

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.is_opened = False
