import numpy as np
import pandas as pd

def forecast_hhs_care(data, horizon=30, test_size=0.20):
    """
    Holt linear trend baseline over ordered reporting observations.
    Forecast horizon means future reporting observations, not calendar days.
    This is a baseline, not a causal or operational capacity forecast.
    """
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    y = data.sort_values("date")["hhs_care"].dropna().astype(float).reset_index(drop=True)
    if len(y) < 30:
        raise ValueError("At least 30 valid observations are required for forecasting.")
    split = max(10, int(len(y) * (1 - test_size)))
    train, test = y.iloc[:split], y.iloc[split:]
    model = ExponentialSmoothing(train, trend="add", damped_trend=True, seasonal=None,
                                 initialization_method="estimated").fit(optimized=True)
    pred = model.forecast(len(test))
    mae = float(np.mean(np.abs(test.to_numpy() - pred.to_numpy())))
    rmse = float(np.sqrt(np.mean((test.to_numpy() - pred.to_numpy()) ** 2)))
    final_model = ExponentialSmoothing(y, trend="add", damped_trend=True, seasonal=None,
                                        initialization_method="estimated").fit(optimized=True)
    future = final_model.forecast(horizon)
    # Approximate prediction interval based on in-sample residual scale; clearly labelled.
    resid = y - final_model.fittedvalues
    sigma = float(resid.std())
    future_dates = pd.date_range(data["date"].max() + pd.Timedelta(days=1), periods=horizon, freq="D")
    result = pd.DataFrame({
        "forecast_step": np.arange(1, horizon + 1),
        "forecast_date_placeholder": future_dates,
        "hhs_care_forecast": future.to_numpy(),
        "lower_approx_95": future.to_numpy() - 1.96 * sigma,
        "upper_approx_95": future.to_numpy() + 1.96 * sigma,
    })
    metrics = {"holdout_mae": mae, "holdout_rmse": rmse, "train_observations": len(train),
               "test_observations": len(test), "forecast_horizon_reporting_observations": horizon}
    return result, metrics, pd.DataFrame({"actual": test, "predicted": pred})
