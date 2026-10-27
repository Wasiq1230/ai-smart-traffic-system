import math
from typing import List, Dict, Any

def evaluate_forecast_metrics(y_true: List[float], y_pred: List[float]) -> Dict[str, float]:
    n = len(y_true)
    if n == 0 or len(y_pred) != n:
        return {"mae": 0.0, "rmse": 0.0, "mape": 0.0, "r2_score": 0.0}

    mae = sum(abs(t - p) for t, p in zip(y_true, y_pred)) / n
    mse = sum((t - p) ** 2 for t, p in zip(y_true, y_pred)) / n
    rmse = math.sqrt(mse)

    mape_vals = [abs(t - p) / max(1.0, abs(t)) for t, p in zip(y_true, y_pred)]
    mape = (sum(mape_vals) / n) * 100.0

    mean_true = sum(y_true) / n
    ss_tot = sum((t - mean_true) ** 2 for t in y_true)
    ss_res = sum((t - p) ** 2 for t, p in zip(y_true, y_pred))
    r2 = 1.0 - (ss_res / max(1e-6, ss_tot)) if ss_tot > 0 else 1.0

    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "mape": round(mape, 2),
        "r2_score": round(max(0.0, min(1.0, r2)), 3),
        "sample_count": n
    }
