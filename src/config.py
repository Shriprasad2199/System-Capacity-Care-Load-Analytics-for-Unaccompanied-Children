from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "HHS_Unaccompanied_Alien_Children_Program.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "uac_cleaned.csv"
FEATURE_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "uac_features.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"

SOURCE_TO_CANONICAL = {
    "Date": "date",
    "Children apprehended and placed in CBP custody*": "cbp_intake",
    "Children in CBP custody": "cbp_custody",
    "Children transferred out of CBP custody": "transfers_to_hhs",
    "Children in HHS Care": "hhs_care",
    "Children discharged from HHS Care": "hhs_discharges",
}
