import yfinance as yf
import pandas as pd
import numpy as np

def get_data(name: list, horizon: str, time: str):
    data: pd.DataFrame = yf.download(tickers = name, period = horizon, interval = time, auto_adjust = False)
    if "Adj Close" in data:
        price: pd.DataFrame = data["Adj Close"]
    else:
        price: pd.DataFrame = data["Close"]
    if price.isna().sum().sum() > 0:
        price.bfill(inplace = True)
        price.ffill(inplace = True)
        price.dropna(inplace = True, how = "any", axis = 1)
    returns: pd.DataFrame = np.log(price).diff().dropna()
    return returns

def get_stats(returns: pd.DataFrame):
    distribution: pd.DataFrame = pd.DataFrame({
       "Skewness": returns.skew(),
       "Kurtosis": returns.kurt()},
       index = returns.columns).T
    return distribution