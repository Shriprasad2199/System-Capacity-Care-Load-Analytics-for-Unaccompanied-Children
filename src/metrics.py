import numpy as np
import pandas as pd

def calculate_kpis(data):
    d = data.sort_values("date")
    latest = d.iloc[-1]
    latest7 = d.tail(7)
    return {
        "latest_date": latest["date"],
        "total_system_load": float(latest["total_system_load"]),
        "cbp_custody": float(latest["cbp_custody"]),
        "hhs_care": float(latest["hhs_care"]),
        "latest_cbp_intake": float(latest["cbp_intake"]),
        "latest_hhs_transfers": float(latest["transfers_to_hhs"]),
        "latest_hhs_discharges": float(latest["hhs_discharges"]),
        "latest_hhs_net_flow": float(latest["hhs_net_flow"]),
        "latest_system_net_flow": float(latest["system_net_flow"]),
        "seven_observation_net_flow": float(latest7["system_net_flow"].sum()),
        "discharge_offset_ratio": float(latest["hhs_discharge_offset_ratio"]) if pd.notna(latest["hhs_discharge_offset_ratio"]) else np.nan,
    }
