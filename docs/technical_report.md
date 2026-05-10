Portfolio Risk Evaluation: Volatility Forecasting and VaR Backtesting

⸻

1. Objective

The objective of this project is to evaluate the impact of volatility model choice on:

* forecast accuracy
* risk estimation (Value-at-Risk)
* backtesting performance

The analysis compares simple and complex models under identical conditions.

⸻

2. Volatility Models

Rolling Volatility

$$
\sigma_t = \mathrm{std}(r_{t-\text{window} : t})
$$

* purely historical
* no dynamics
* high estimation noise

⸻

EWMA

$$
\sigma_t^2 = \lambda \sigma_{t-1}^2 + (1 - \lambda) r_{t-1}^2
$$

* captures volatility clustering
* no parameter estimation required
* robust and stable

⸻

GARCH(1,1)

$$
\sigma_t^2 = \omega + \alpha r_{t-1}^2 + \beta \sigma_{t-1}^2
$$

* explicitly models conditional heteroskedasticity
* requires numerical estimation
* sensitive to sample size and noise

⸻

3. Forecasting Framework

* rolling window: 60 days
* models re-estimated at each time step
* 1-step ahead volatility forecast
* Realized volatility is proxied by the 20-day forward rolling standard deviation, a standard choice in the empirical volatility literature.

All models produce:

$$
\hat{\sigma}_{t+1}
$$

⸻

4. Evaluation Metrics

Forecast accuracy is evaluated using:

MAE:
$$
|\sigma_t - \hat{\sigma}_t|
$$

RMSE:
$$
\sqrt{(\sigma_t - \hat{\sigma}_t)^2}
$$

QLIKE:
$$
\log(\hat{\sigma}_t^2) + \frac{\sigma_t^2}{\hat{\sigma}_t^2}
$$

QLIKE penalizes both over and under-estimation of variance, with stronger penalties for underestimation.
QLIKE is coherent with log-likelihood under Gaussian assumption

⸻

5. VaR Estimation

VaR is defined as the left-tail quantile of returns:

$$
\mathrm{VaR}_\alpha = q_\alpha(r_t)
$$

Assuming conditional normality:

$$
\mathrm{VaR}_t = z_\alpha \hat{\sigma}_t
$$

To account for non-normality, the Cornish-Fisher expansion is used:

$$
z_{CF} = z + \text{skew/kurtosis corrections}
$$

Important:

* skewness and kurtosis are estimated over the full sample (static)
* VaR is therefore not fully conditional
* VaR represents a negative return threshold
* violations occur when realized returns fall below this level.

⸻

6. Backtesting

Violation

A violation occurs when:

$$
r_t < \mathrm{VaR}_t
$$

⸻

Kupiec Test (Unconditional Coverage)

H0: violation rate = α

Tests whether the observed frequency of violations matches the expected level.

⸻

Christoffersen Test (Independence)

Tests whether violations are independent over time.

Note:

In this dataset, the test is always unstable due to insufficient transition observations (no consecutive violations)

⸻

7. Results

Volatility Forecasting

* EWMA achieves the lowest MAE, RMSE, and QLIKE
* GARCH does not improve performance despite higher complexity
* Rolling volatility is the least accurate

⸻

VaR Backtesting

* All models produce violation rates above 5%, all models are ~6%
* This indicates systematic underestimation of risk
* Rolling volatility shows slightly better coverage
* However, none of the models passes coverage tests consistently

⸻

Kupiec Test

* The majority of assets fail the Kupiec test, indicating that the observed violation rates differ significantly from the nominal level.
* GARCH and EWMA only 8 assets pass the test
* 11 assets pass the test with Rolling volatility
* this result highlight a trade-off between forecast accuracy and VaR calibration.

⸻

8. Economic Interpretation

* Estimation error dominates model complexity
* GARCH introduces parameter uncertainty without improving forecasts
* EWMA provides a robust trade-off between simplicity and accuracy

Crucially:

* Accurate volatility forecasts do not guarantee accurate risk measures
* VaR calibration depends on tail behavior, not only variance

⸻

9. Limitations

* static higher moments (Cornish-Fisher)
* no tail-specific modeling (e.g. Extreme Value Theory)
* small rolling window (60 days) increases noise
* GARCH refitting introduces instability
* asymmetric volatility models (e.g. GJR-GARCH) are not considered
* Realized volatility is proxied by the 20-day forward rolling standard deviation, a standard choice in the empirical volatility literature.

⸻

10. Conclusion

* EWMA is the most effective model for volatility forecasting
* All models fail to produce correctly calibrated VaR

Implication:

* increasing model complexity does not necessarily improve risk estimation
* robust, simple models often outperform in noisy environments