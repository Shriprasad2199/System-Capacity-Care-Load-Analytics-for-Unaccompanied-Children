import pandas as pd
from src.feature_engineering import add_features

def test_system_load_and_net_flow():
    d = pd.DataFrame({
        "date": pd.to_datetime(["2024-01-01"]),
        "cbp_intake": [10], "cbp_custody": [20], "transfers_to_hhs": [8],
        "hhs_care": [100], "hhs_discharges": [6]
    })
    out = add_features(d)
    assert out.total_system_load.iloc[0] == 120
    assert out.hhs_net_flow.iloc[0] == 2
    assert out.system_net_flow.iloc[0] == 4
