import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox

def diagnostic(returns: pd.DataFrame):
    results = {}
    for c in returns.columns:
        lb_resid = acorr_ljungbox(returns[c], lags=[5], return_df=True)["lb_pvalue"].iloc[0]
        lb_sq = acorr_ljungbox(returns[c]**2, lags=[5], return_df=True)["lb_pvalue"].iloc[0]
        results[c] = {
            "autocorr_pval": lb_resid,
            "arch_effect_pval": lb_sq
        }
    return pd.DataFrame(results).T