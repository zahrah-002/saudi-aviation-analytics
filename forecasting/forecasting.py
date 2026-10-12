"""Saudi Aviation | Time Series Forecasting & Analytics.

Reproduces the user's Colab workflow:
- 2023–2024 training, 2025 holdout and rolling one-step evaluation
- Seasonal Naive, ETS additive, SARIMA(2,1,0)(1,0,0,12)
- ADF, STL, forecast intervals, 2026 forecasts and Power BI export

Run: pip install -r forecasting/requirements.txt
     python forecasting/forecasting.py
Outputs are saved to forecasting/output/ (ignored by Git).
"""
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX

BASE = Path(__file__).resolve().parent
DATA = BASE / "Saudi_Aviation_Monthly_2023_2025_Forecasting.csv"
OUTPUT = BASE / "output"
OUTPUT.mkdir(exist_ok=True)
SARIMA_ORDER = (2, 1, 0)
SARIMA_SEASONAL = (1, 0, 0, 12)


def scores(actual, predicted):
    a, p = np.asarray(actual, dtype=float), np.asarray(predicted, dtype=float)
    denom = np.abs(a) + np.abs(p)
    smape = np.mean(np.divide(200 * np.abs(a - p), denom,
                             out=np.zeros_like(a), where=denom > 0))
    return {"MAE": mean_absolute_error(a, p),
            "RMSE": np.sqrt(mean_squared_error(a, p)),
            "sMAPE (%)": smape}


def fit_ets(history):
    return ExponentialSmoothing(
        history, trend="add", seasonal="add", seasonal_periods=12,
        initialization_method="estimated",
    ).fit(optimized=True)


def fit_sarima(history):
    return SARIMAX(
        history, order=SARIMA_ORDER, seasonal_order=SARIMA_SEASONAL,
        enforce_stationarity=False, enforce_invertibility=False,
    ).fit(disp=False)


def main():
    df = pd.read_csv(DATA, parse_dates=["date"]).sort_values("date")
    expected = pd.date_range("2023-01-01", "2025-12-01", freq="MS")
    if len(df) != 36 or not pd.DatetimeIndex(df["date"]).equals(expected):
        raise ValueError("Expected 36 unique consecutive months: Jan 2023–Dec 2025.")
    if df["passengers"].isna().any() or (df["passengers"] < 0).any():
        raise ValueError("Monthly passengers must be nonnegative and non-null.")
    ts = df.set_index("date")["passengers"].astype(float).asfreq("MS")
    train, test = ts.iloc[:24], ts.iloc[24:]
    print("Monthly observations:", len(ts))
    print("Airport coverage:", df["airports_with_records"].min(),
          "to", df["airports_with_records"].max())
    print("Source passenger fields missing:", df["missing_passenger_values"].sum())

    for label, series in [("Original", ts), ("First difference", ts.diff().dropna())]:
        adf = adfuller(series, autolag="AIC", result_object=False)
        print(label, "ADF:", round(adf[0], 4), "p-value:", f"{adf[1]:.8g}")
    # Exploratory only: three seasonal cycles are insufficient to establish robust seasonality.
    decomposition = STL(ts, period=12, robust=True).fit()
    pd.DataFrame({"trend": decomposition.trend, "seasonal": decomposition.seasonal,
                  "residual": decomposition.resid}).to_csv(
        OUTPUT / "stl_decomposition.csv", encoding="utf-8-sig")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        naive = pd.Series(train.iloc[-12:].to_numpy(), index=test.index)
        ets_fit = fit_ets(train)
        sarima_fit = fit_sarima(train)
        candidates = {
            "Seasonal Naive": naive,
            "ETS": pd.Series(ets_fit.forecast(12).to_numpy(), index=test.index),
            "SARIMA": pd.Series(sarima_fit.forecast(12).to_numpy(), index=test.index),
        }
        holdout_rows, holdout_preds = [], pd.DataFrame(
            {"date": test.index, "actual": test.to_numpy()})
        for name, prediction in candidates.items():
            holdout_rows.append({"model": name, **scores(test, prediction)})
            holdout_preds[name] = prediction.to_numpy()
        holdout_scores = pd.DataFrame(holdout_rows).sort_values("MAE")
        holdout_scores.to_csv(OUTPUT / "model_comparison_2025.csv", index=False)
        holdout_preds.to_csv(OUTPUT / "backtest_2025.csv", index=False)
        print("\n2025 12-month holdout:\n", holdout_scores.to_string(index=False))

        rolling = []
        for date in test.index:
            history = ts.loc[:date - pd.offsets.MonthBegin(1)]
            rolling.append({
                "date": date,
                "actual": float(ts.loc[date]),
                "Seasonal Naive": float(history.iloc[-12]),
                "ETS": float(fit_ets(history).forecast(1).iloc[0]),
                "SARIMA": float(fit_sarima(history).forecast(1).iloc[0]),
            })
        rolling_df = pd.DataFrame(rolling)
        rolling_df.to_csv(OUTPUT / "rolling_predictions_2025.csv", index=False)
        rolling_scores = pd.DataFrame([
            {"model": name, **scores(rolling_df["actual"], rolling_df[name])}
            for name in candidates
        ]).sort_values("MAE")
        rolling_scores.to_csv(OUTPUT / "rolling_scores_2025.csv", index=False)
        print("\n2025 rolling one-month-ahead:\n", rolling_scores.to_string(index=False))

        # Assess 2025 95% intervals using the model fit only through 2024.
        test_ci = sarima_fit.get_forecast(steps=12).conf_int(alpha=0.05)
        coverage = pd.DataFrame({
            "date": test.index, "actual": test.to_numpy(),
            "lower_95": test_ci.iloc[:, 0].to_numpy(),
            "upper_95": test_ci.iloc[:, 1].to_numpy(),
        })
        coverage["covered"] = (
            (coverage["actual"] >= coverage["lower_95"])
            & (coverage["actual"] <= coverage["upper_95"])
        )
        coverage.to_csv(OUTPUT / "interval_coverage_2025.csv", index=False)
        print("\n2025 interval coverage:",
              int(coverage["covered"].sum()), "/ 12 months")

        # Refit to the entire 2023–2025 history for Jan–Dec 2026 scenarios.
        ets_final = fit_ets(ts)
        sarima_final = fit_sarima(ts)
        horizon = pd.date_range("2026-01-01", periods=12, freq="MS")
        ets_2026 = ets_final.forecast(12)
        sarima_result = sarima_final.get_forecast(steps=12)
        sarima_2026 = sarima_result.predicted_mean
        intervals = sarima_result.conf_int(alpha=0.05)
        forecast = pd.DataFrame({
            "date": horizon, "ETS": ets_2026.to_numpy(),
            "SARIMA": sarima_2026.to_numpy(),
            "lower_95": intervals.iloc[:, 0].to_numpy(),
            "upper_95": intervals.iloc[:, 1].to_numpy(),
        })
        forecast.to_csv(OUTPUT / "forecast_2026.csv", index=False)
        print("\n2026 ETS total:", f"{forecast['ETS'].sum():,.0f}")
        print("2026 SARIMA total:", f"{forecast['SARIMA'].sum():,.0f}")

        # Long table: actual history once, each 2026 forecast once.
        actual = pd.DataFrame({
            "date": ts.index, "passengers": ts.to_numpy(),
            "data_type": "Actual", "model": "Historical",
            "lower_95": np.nan, "upper_95": np.nan,
        })
        sarima_export = pd.DataFrame({
            "date": horizon, "passengers": forecast["SARIMA"].to_numpy(),
            "data_type": "Forecast", "model": "SARIMA",
            "lower_95": forecast["lower_95"].to_numpy(),
            "upper_95": forecast["upper_95"].to_numpy(),
        })
        ets_export = pd.DataFrame({
            "date": horizon, "passengers": forecast["ETS"].to_numpy(),
            "data_type": "Forecast", "model": "ETS",
            "lower_95": np.nan, "upper_95": np.nan,
        })
        powerbi = pd.concat([actual, sarima_export, ets_export], ignore_index=True)
        powerbi["year"] = powerbi["date"].dt.year
        powerbi["month_number"] = powerbi["date"].dt.month
        powerbi.sort_values(["date", "model"]).to_csv(
            OUTPUT / "Saudi_Aviation_PowerBI_Forecasting.csv",
            index=False, encoding="utf-8-sig",
        )
        print("\nPower BI rows:", len(powerbi), "(36 actual + 24 forecast)")


if __name__ == "__main__":
    main()
