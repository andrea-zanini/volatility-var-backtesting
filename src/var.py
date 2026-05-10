import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from scipy import stats
import pandas as pd
from config import alpha, models

def var(forecast_volatility: dict, stats_distribution: pd.DataFrame):
    VaR = {model: {} for model in models}
    z = stats.norm.ppf(alpha)
    for column in stats_distribution.columns:
        skew = stats_distribution[column].iloc[0]
        kurt = stats_distribution[column].iloc[1]
        z_cf = (z + (z**2 - 1) * skew / 6 +
        (z**3 - 3 * z) * kurt / 24 -
        (2 * z**3 - 5*z) * skew**2 / 36)
        for model in models:
            VaR[model][column] = z_cf * forecast_volatility[model][column]
    VaR = {model: pd.DataFrame(VaR[model]) for model in models}
    return VaR