import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from scipy import stats
import pandas as pd
import numpy as np
from config import models, alpha

def backtest(returns: pd.DataFrame, var: dict):
    violation_stats = []
    hits = {model : {} for model in models}
    for model in models:
        ret = returns.shift(-1).loc[var[model].index].dropna()
        fv = var[model].loc[ret.index]
        assert all(ret.index == fv.index)
        for column in returns.columns:
           hits[model][column] = (ret[column] < fv[column]).astype(int)
           violation_stats.append({
               "ticker": column,
               "model": model,
               "T": len(ret),
               "violation rate": (ret[column] < fv[column]).mean(),
               "violation": (ret[column] < fv[column]).sum()})
    hits = {model: pd.DataFrame(hits[model]) for model in models}
    return pd.DataFrame(violation_stats).set_index(["ticker", "model"]), hits

def kupiec_test(stats_violation: pd.DataFrame):
    p_value = []
    for (ticker, model), rows in stats_violation.iterrows():
        T = rows["T"]
        N = rows["violation"]
        v = rows["violation rate"]
        if N == 0 or N == T:
            p_value.append({
                "ticker": ticker,
                "model": model,
                "p-value": np.nan,
                "reject H0": np.nan
            })
            continue
        LR = -2 * ((T - N) * np.log(1 - alpha) + N * np.log(alpha) -
                   (T - N) * np.log(1 - v) - N * np.log(v))
        p_value.append({
            "ticker": ticker,
            "model": model,
            "p-Value": 1 - stats.chi2.cdf(LR, df = 1),
            "reject p-value": 1 - stats.chi2.cdf(LR, df = 1) < 0.05})
    return pd.DataFrame(p_value).set_index(["ticker", "model"])

def christoffersen_test(hits: dict):
    p_value = []
    for model in models:
        for column in hits[model].columns:
            hits_series = hits[model][column]
            n_00 = ((hits_series[:-1] == 0) & (hits_series[1:] == 0)).sum()
            n_01 = ((hits_series[:-1] == 0) & (hits_series[1:] == 1)).sum()
            n_10 = ((hits_series[:-1] == 1) & (hits_series[1:] == 0)).sum()
            n_11 = ((hits_series[:-1] == 1) & (hits_series[1:] == 1)).sum()
            p_01 = n_01 / (n_00 + n_01)
            p_11 = n_11 / (n_10 + n_11)
            p = (n_01 + n_11) / (n_00 + n_01 + n_10 + n_11)
            if n_00 + n_01 == 0 or n_10 + n_11 == 0 or p_01 == 0 or p_11 == 0:
                p_value.append({
                    "ticker": column,
                    "model": model,
                    "LR": np.nan,
                    "p_value": np.nan,
                    "reject H0": np.nan
                })
                continue
            LR = -2 * ((n_00 + n_10) * np.log(1 - p) + (n_01 + n_11) * np.log(p) -
                    n_00 * np.log(1 - p_01) - n_01 * np.log(p_01) -
                    n_10 * np.log(1 - p_11) - n_11 * np.log(p_11))
            p_value.append({
            "ticker": column,
            "model": model,
            "p-Value": 1 - stats.chi2.cdf(LR, df=1),
            "reject p-value": 1 - stats.chi2.cdf(LR, df = 1) < 0.05})
    return pd.DataFrame(p_value).set_index(["ticker", "model"])