import pandas as pd
from .preprocessing import NUMERIC_COLUMNS

def data_quality_report(data):
    """Return auditable data-quality checks; gaps are reported, not filled."""
    gaps = data["date"].sort_values().diff().dt.days.dropna()
    report = {
        "rows": int(len(data)),
        "duplicate_dates": int(data["date"].duplicated().sum()),
        "missing_dates": int(data["date"].isna().sum()),
        "missing_numeric_cells": int(data[NUMERIC_COLUMNS].isna().sum().sum()),
        "negative_numeric_cells": int((data[NUMERIC_COLUMNS] < 0).sum().sum()),
        "minimum_reporting_gap_days": int(gaps.min()) if len(gaps) else None,
        "median_reporting_gap_days": float(gaps.median()) if len(gaps) else None,
        "maximum_reporting_gap_days": int(gaps.max()) if len(gaps) else None,
        "consecutive_calendar_observations": int((gaps == 1).sum()),
    }
    return report

def stock_flow_reconciliation(data):
    """Compare observed stock changes with simple flow identities on consecutive dates only."""
    d = data.sort_values("date").copy()
    d["gap_days"] = d["date"].diff().dt.days
    d["cbp_stock_change"] = d["cbp_custody"].diff()
    d["cbp_implied_change"] = d["cbp_intake"] - d["transfers_to_hhs"]
    d["hhs_stock_change"] = d["hhs_care"].diff()
    d["hhs_implied_change"] = d["transfers_to_hhs"] - d["hhs_discharges"]
    consecutive = d[d["gap_days"] == 1].copy()
    if consecutive.empty:
        return consecutive
    consecutive["cbp_reconciliation_error"] = consecutive["cbp_stock_change"] - consecutive["cbp_implied_change"]
    consecutive["hhs_reconciliation_error"] = consecutive["hhs_stock_change"] - consecutive["hhs_implied_change"]
    return consecutive
