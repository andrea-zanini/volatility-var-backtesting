import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import pandas as pd
import numpy as np
from src.volatility import target_volatility
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from config import models

def metrics(returns: pd.DataFrame, forecast_volatility: dict):
    realized_volatility = target_volatility(returns).dropna()
    common_index = realized_volatility.index.intersection(forecast_volatility["garch"].index)
    realized_volatility = realized_volatility.loc[common_index]
    forecast_volatility_aligned = {
        model: forecast_volatility[model].loc[common_index] for model in models
    }
    result = []
    eps = 1e-8
    realized_volatility = realized_volatility.clip(lower = eps)
    for column in returns.columns:
        for model in models:
            result.append({
                "ticker": column,
                "model": model,
                "MAE": mean_absolute_error(realized_volatility[column], forecast_volatility_aligned[model][column]),
                "RMSE": root_mean_squared_error(realized_volatility[column], forecast_volatility_aligned[model][column]),
                "Q-LIKE": (np.log(forecast_volatility_aligned[model][column]**2) + realized_volatility[column]**2 / forecast_volatility_aligned[model][column]**2).mean()
            })
    metrics = pd.DataFrame(result).set_index(["ticker", "model"])
    return metrics