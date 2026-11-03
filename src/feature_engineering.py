import numpy as np
import pandas as pd

def add_features(data):
    """Create interpretable operational measures. Rolling windows count observations, not days."""
    d = data.sort_values("date").copy()
    d["total_system_load"] = d["cbp_custody"] + d["hhs_care"]
    d["hhs_net_flow"] = d["transfers_to_hhs"] - d["hhs_discharges"]
    # Internal transfers cancel when measuring the combined CBP + HHS system.
    d["system_net_flow"] = d["cbp_intake"] - d["hhs_discharges"]
    d["hhs_discharge_offset_ratio"] = np.where(
        d["transfers_to_hhs"] > 0, d["hhs_discharges"] / d["transfers_to_hhs"], np.nan
    )
    d["system_load_change"] = d["total_system_load"].diff()
    d["system_load_pct_change"] = d["total_system_load"].pct_change() * 100
    d["hhs_care_pct_change"] = d["hhs_care"].pct_change() * 100
    for window in (7, 14):
        d[f"hhs_care_rolling_mean_{window}obs"] = d["hhs_care"].rolling(window, min_periods=window).mean()
        d[f"hhs_care_rolling_std_{window}obs"] = d["hhs_care"].rolling(window, min_periods=window).std()
        d[f"system_load_rolling_mean_{window}obs"] = d["total_system_load"].rolling(window, min_periods=window).mean()
        d[f"system_net_flow_sum_{window}obs"] = d["system_net_flow"].rolling(window, min_periods=window).sum()
    d["care_load_volatility_index"] = (
        d["hhs_care_rolling_std_7obs"] / d["hhs_care_rolling_mean_7obs"].replace(0, np.nan)
    ) * 100
    # A transparent, data-relative flag, not a legal or facility-capacity threshold.
    threshold = d["total_system_load"].quantile(0.90)
    d["high_system_load_flag"] = d["total_system_load"] >= threshold
    d["sustained_positive_net_flow_flag"] = d["system_net_flow_sum_7obs"] > 0
    d["reporting_gap_days"] = d["date"].diff().dt.days
    d["year_month"] = d["date"].dt.to_period("M").astype(str)
    d["year"] = d["date"].dt.year
    return d
