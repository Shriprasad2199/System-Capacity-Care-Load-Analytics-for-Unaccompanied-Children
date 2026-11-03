import pandas as pd
from .config import RAW_DATA_PATH, SOURCE_TO_CANONICAL

def load_raw_data(path=RAW_DATA_PATH):
    """Load the source CSV without changing the original file."""
    return pd.read_csv(path)

def standardise_columns(df):
    missing = [c for c in SOURCE_TO_CANONICAL if c not in df.columns]
    if missing:
        raise ValueError(f"Required source columns are missing: {missing}")
    return df.rename(columns=SOURCE_TO_CANONICAL).copy()
