from config import tickers, periods, frequency, models
from src.data import get_data, get_stats
from src.test import diagnostic
from src.forecast import rolling_forecast
from src.metrics import metrics
from src.sanity_check import nan, positivity
from src.var import var
from src.backtest import backtest, kupiec_test, christoffersen_test
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
stats_path = BASE_DIR / "results" / "stats"
stats_path.mkdir(parents = True, exist_ok = True)
stats_var_path = BASE_DIR / "results" / "var"
stats_var_path.mkdir(parents = True, exist_ok = True)
violation_path = BASE_DIR / "results" / "violation rate"
violation_path.mkdir(parents = True, exist_ok = True)
test_kupiec_path = BASE_DIR / "results" / "kupiec"
test_kupiec_path.mkdir(parents = True, exist_ok = True)
hits_path = BASE_DIR / "results" / "hits"
hits_path.mkdir(parents = True, exist_ok = True)
forecast_path = BASE_DIR / "results" / "forecast"
forecast_path.mkdir(parents = True, exist_ok = True)
returns_path = BASE_DIR / "results" / "returns"
returns_path.mkdir(parents = True, exist_ok = True)

log_returns = get_data(tickers, periods, frequency)
nan(log_returns)
distribution_stats = get_stats(log_returns)
test = diagnostic(log_returns)
forecast_volatility = rolling_forecast(log_returns)
for model in models:
    positivity(forecast_volatility[model])
stats = metrics(log_returns, forecast_volatility)
VaR = var(forecast_volatility, distribution_stats)
violation_stats, hits = backtest(log_returns, VaR)
test_kupiec = kupiec_test(violation_stats)
test_christoffersen = christoffersen_test(hits) 
stats.to_parquet(stats_path / f"metriche_modelli.parquet")
violation_stats.to_parquet(violation_path / f"violation.parquet")
test_kupiec.to_parquet(test_kupiec_path / f"kupiec.parquet")
for model in models:
    VaR[model].to_parquet(stats_var_path / f"var{model}.parquet")
for model in models:
    hits[model].to_parquet(hits_path / f"hits{model}.parquet")
for model in models:
    forecast_volatility[model].to_parquet(forecast_path / f"forecast{model}.parquet")
log_returns.to_parquet(returns_path / f"returns.parquet")