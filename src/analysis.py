import pandas as pd

def monthly_summary(data):
    """Monthly means for stocks and sums of observed flows; includes observation coverage."""
    return (data.set_index("date").resample("MS")
            .agg(cbp_intake=("cbp_intake", "sum"),
                 cbp_custody_mean=("cbp_custody", "mean"),
                 transfers_to_hhs=("transfers_to_hhs", "sum"),
                 hhs_care_mean=("hhs_care", "mean"),
                 hhs_discharges=("hhs_discharges", "sum"),
                 total_system_load_mean=("total_system_load", "mean"),
                 system_net_flow=("system_net_flow", "sum"),
                 reporting_observations=("cbp_intake", "count"))
            .reset_index())

def period_summary(data, period="year"):
    if period == "year":
        return data.groupby("year").agg(
            observations=("date", "count"),
            mean_system_load=("total_system_load", "mean"),
            mean_hhs_care=("hhs_care", "mean"),
            total_intake_observed=("cbp_intake", "sum"),
            total_discharges_observed=("hhs_discharges", "sum"),
            mean_hhs_net_flow=("hhs_net_flow", "mean")
        ).reset_index()
    raise ValueError("Supported period: year")
