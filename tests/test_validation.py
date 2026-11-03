import pandas as pd
from src.validation import data_quality_report

def test_quality_report_detects_reporting_gap():
    d = pd.DataFrame({
        "date": pd.to_datetime(["2024-01-01", "2024-01-03"]),
        "cbp_intake": [1, 2], "cbp_custody": [1, 2],
        "transfers_to_hhs": [1, 1], "hhs_care": [10, 11],
        "hhs_discharges": [0, 1],
    })
    report = data_quality_report(d)
    assert report["maximum_reporting_gap_days"] == 2
