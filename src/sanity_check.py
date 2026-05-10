import pandas as pd

def nan(returns):
    assert returns.isna().sum().sum() == 0

def positivity(volatility: pd.DataFrame):
    assert (volatility > 0 ).all().all()