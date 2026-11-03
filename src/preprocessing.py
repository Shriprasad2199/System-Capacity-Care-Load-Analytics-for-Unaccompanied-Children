import pandas as pd
from .data_loader import load_raw_data, standardise_columns
from .config import PROCESSED_DATA_PATH

NUMERIC_COLUMNS = ["cbp_intake", "cbp_custody", "transfers_to_hhs", "hhs_care", "hhs_discharges"]

def clean_data(df=None):
    """Remove fully blank records, parse dates, convert counts, sort chronologically."""
    if df is None:
        df = load_raw_data()
    data = standardise_columns(df)
    data = data.dropna(how="all").copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.dropna(subset=["date"]).copy()
    for col in NUMERIC_COLUMNS:
        data[col] = pd.to_numeric(
            data[col].astype("string").str.replace(",", "", regex=False).str.strip(),
            errors="coerce"
        )
    data = data.sort_values("date").reset_index(drop=True)
    return data

def save_clean_data(data, path=PROCESSED_DATA_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path, index=False)
