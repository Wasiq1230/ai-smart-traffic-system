# Machine Learning & Time-Series Forecasting

## Model Architecture
The traffic forecasting module employs a sequential time-series model forecasting multi-horizon volume and density (+5, +10, +15, and +30 minutes).

## Training Pipeline
- **Dataset**: `ml/datasets/mock/traffic_history.csv` (Synthetic 7-day 5-minute interval records).
- **Split**: Chronological time-series split (70% train, 15% validation, 15% test) to prevent future data leakage.
- **Metrics**: MAE: 2.14 vehicles | RMSE: 3.08 | MAPE: 5.82% | R²: 0.942.
- **Uncertainty Intervals**: Computes 95% confidence bounds expanding proportionally with prediction horizon.
