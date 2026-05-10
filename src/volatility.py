import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import pandas as pd
import numpy as np
from arch import arch_model
import os
from contextlib import contextmanager  
from config import lambda_

def rolling_volatility(train: pd.DataFrame):
    sigma_t = train.std()
    return sigma_t

def ewma(train: pd.DataFrame):
    sigma_t: pd.DataFrame = np.sqrt(train.pow(2).ewm(alpha = 1-lambda_).mean()).iloc[-1]
    return sigma_t

@contextmanager  
def suppress_output():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

def garch(train: pd.DataFrame):
    sigma_t = []
    for columns in train.columns:
        with suppress_output():
            var_t = arch_model(train[columns], mean = "Zero", vol = "GARCH", p = 1, q = 1).fit(disp = "off")
            forecast = var_t.forecast(horizon = 1)
            sigma = np.sqrt(forecast.variance.iloc[-1, 0])
            sigma_t.append(sigma)
    return pd.Series(sigma_t, index=train.columns)

def target_volatility(returns: pd.DataFrame):
    sigma_t = returns.rolling(20).std().shift(-1)
    return sigma_t