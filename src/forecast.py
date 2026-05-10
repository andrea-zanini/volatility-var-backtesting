import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import pandas as pd
from src.volatility import rolling_volatility, ewma, garch
from config import window, models

def rolling_forecast(returns: pd.DataFrame):
    volatility_forecasts = {model: [] for model in models}
    for t in range(window, len(returns)):
        train_set = returns.iloc[t - window : t]
        for model in models:
            if model == "rolling":
                sigma = rolling_volatility(train_set)
            elif model == "ewma":
                sigma = ewma(train_set)
            elif model == "garch":
                sigma = garch(train_set)
            volatility_forecasts[model].append(sigma)
    return {model: pd.DataFrame(volatility_forecasts[model], index = returns.index[window:]) for model in models}