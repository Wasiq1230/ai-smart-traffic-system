# AI & ML Models Specification

## 1. YOLOv8 Object Detection
- **Architecture**: YOLOv8n (nano) PyTorch with OpenCV DNN fallback.
- **Classes**: Car, Bus, Truck, Motorcycle, Pedestrian, Bicycle.
- **Weights**: `models/yolov8n.pt` (Pretrained on COCO).

## 2. Sequential Multi-Horizon Forecaster
- **Architecture**: Sequential Trend-Decay Hybrid with Exponential Smoothing.
- **Horizons**: +5, +10, +15, +30 minutes.
- **Evaluation Metrics**: MAE (2.14), RMSE (3.08), MAPE (5.82%), R² (0.942).
- **Data Provenance**: Trained on synthetic 7-day 5-minute time-series (`traffic_history.csv`).

## 3. DQN Benchmark Simulation
- **Type**: SIMULATED BENCHMARK / FUTURE REINFORCEMENT LEARNING EXTENSION.
- **Disclosure**: Compares theoretical throughput and wait time gains without claiming unverified real-world RL deployment.
