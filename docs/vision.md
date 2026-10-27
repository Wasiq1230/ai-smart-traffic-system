# AI Vision Subsystem

## Overview
The AI Vision layer complies with the `AI_VISON.DOCX` modular specification.

## Pipeline Components
1. **VideoProcessor**: Manages frame ingestion, resolution normalization (640x480), FPS pacing, and camera fallback.
2. **ModelLoader**: Multi-backend YOLOv8 loader supporting Ultralytics PyTorch, ONNX Runtime, and OpenCV DNN.
3. **YOLODetector**: Vehicle and Vulnerable Road User (VRU) detection (cars, buses, trucks, motorcycles, pedestrians, cyclists).
4. **SimpleTracker**: Spatial association & IoU tracking with trajectory history and speed estimation.
5. **VehicleCounter**: Unique vehicle deduplication, directional counting, and class breakdown.
6. **LaneDetector**: Polygon-based centroid containment and queue measurement.
7. **EmergencyDetector**: Ambulance, fire truck, and police identification with visual flashing beacon analysis.
8. **AccidentDetector**: Stationary vehicle obstruction and collision-overlap monitoring.
9. **ViolationDetector**: Red-light jumping and speeding infraction detection.
10. **ANPRSystem**: Automated license plate detection and OCR character extraction.
