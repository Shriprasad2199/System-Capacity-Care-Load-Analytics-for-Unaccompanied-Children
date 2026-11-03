from .preprocessing import clean_data, save_clean_data
from .validation import data_quality_report, stock_flow_reconciliation
from .feature_engineering import add_features
from .config import FEATURE_DATA_PATH, OUTPUT_DIR
import json

def main():
    clean = clean_data()
    save_clean_data(clean)
    features = add_features(clean)
    FEATURE_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(FEATURE_DATA_PATH, index=False)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "data_quality_report.json").write_text(json.dumps(data_quality_report(clean), indent=2, default=str))
    stock_flow_reconciliation(clean).to_csv(OUTPUT_DIR / "stock_flow_reconciliation.csv", index=False)
    print(f"Pipeline complete: {len(clean)} usable observations.")
    print(data_quality_report(clean))

if __name__ == "__main__":
    main()
