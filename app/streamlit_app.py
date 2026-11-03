import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.config import RAW_DATA_PATH
from src.preprocessing import clean_data
from src.validation import data_quality_report, stock_flow_reconciliation
from src.feature_engineering import add_features
from src.metrics import calculate_kpis
from src.analysis import monthly_summary
from src.forecasting import forecast_hhs_care

st.set_page_config(page_title="UAC System Capacity Analytics", page_icon="📊", layout="wide")
st.title("System Capacity & Care Load Analytics")
st.caption("Operational analysis of CBP custody, HHS care, transfers and discharges")

@st.cache_data
def get_data():
    return add_features(clean_data())

data = get_data()
min_date, max_date = data.date.min().date(), data.date.max().date()

with st.sidebar:
    st.header("Dashboard filters")
    date_range = st.date_input("Reporting date range", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    else:
        start, end = pd.Timestamp(min_date), pd.Timestamp(max_date)
    selected = data[data.date.between(start, end)].copy()
    st.caption("Rolling windows use reporting observations, not calendar days.")

if selected.empty:
    st.warning("No observations exist in the selected date range.")
    st.stop()

k = calculate_kpis(selected)
a,b,c,d = st.columns(4)
a.metric("Latest total system load", f"{k['total_system_load']:,.0f}")
b.metric("CBP custody", f"{k['cbp_custody']:,.0f}")
c.metric("HHS care", f"{k['hhs_care']:,.0f}")
d.metric("Latest system net flow", f"{k['latest_system_net_flow']:+,.0f}",
         help="CBP intake minus HHS discharges. Transfers are internal to the combined system.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "System overview", "CBP vs HHS", "Flow & backlog", "Pressure indicators", "Data quality & forecast"
])

with tab1:
    st.subheader("Combined system load")
    fig = px.line(selected, x="date", y="total_system_load", title="Total children in CBP custody and HHS care")
    st.plotly_chart(fig, use_container_width=True)
    st.info("This is a system-load measure, not a facility occupancy rate. Facility capacity data is not supplied.")
    monthly = monthly_summary(selected)
    fig2 = px.bar(monthly, x="date", y="total_system_load_mean", title="Monthly mean total system load")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("CBP custody and HHS care")
    long = selected.melt(id_vars="date", value_vars=["cbp_custody","hhs_care"],
                         var_name="stage", value_name="children")
    fig = px.line(long, x="date", y="children", color="stage", title="Active stock by programme stage")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(selected[["date","cbp_custody","hhs_care","total_system_load"]], use_container_width=True)

with tab3:
    st.subheader("Operational flows")
    flows = selected.melt(id_vars="date", value_vars=["cbp_intake","transfers_to_hhs","hhs_discharges"],
                          var_name="flow", value_name="children")
    st.plotly_chart(px.line(flows, x="date", y="children", color="flow",
                            title="Observed intake, transfers and discharges"), use_container_width=True)
    st.plotly_chart(px.bar(selected, x="date", y="system_net_flow",
                           title="System net flow: CBP intake minus HHS discharge"), use_container_width=True)
    st.metric("Cumulative observed system net flow", f"{selected.system_net_flow.sum():+,.0f}")

with tab4:
    st.subheader("Capacity pressure indicators")
    x,y,z = st.columns(3)
    x.metric("High-load observations", f"{int(selected.high_system_load_flag.sum()):,}")
    y.metric("90th percentile load threshold", f"{data.total_system_load.quantile(.90):,.0f}")
    z.metric("Latest 7-observation net flow", f"{selected.tail(7).system_net_flow.sum():+,.0f}")
    st.caption("High load is defined relative to the full dataset's 90th percentile. It is a statistical flag, not an official capacity limit.")
    st.plotly_chart(px.line(selected, x="date", y="care_load_volatility_index",
                            title="HHS care-load volatility index (7-observation coefficient of variation)"),
                    use_container_width=True)
    st.dataframe(selected[["date","total_system_load","system_net_flow_sum_7obs",
                           "care_load_volatility_index","high_system_load_flag",
                           "sustained_positive_net_flow_flag"]], use_container_width=True)

with tab5:
    st.subheader("Data quality")
    report = data_quality_report(clean_data())
    st.json(report)
    rec = stock_flow_reconciliation(clean_data())
    if not rec.empty:
        st.write("Stock-flow reconciliation errors on consecutive calendar dates")
        st.write(rec[["date","cbp_reconciliation_error","hhs_reconciliation_error"]].describe())
    st.subheader("HHS care baseline forecast")
    st.warning("Forecast steps represent future reporting observations. The source dates are irregular, so these are not reliable calendar-day forecasts.")
    horizon = st.slider("Number of future reporting observations", 7, 60, 30)
    if st.button("Run baseline forecast"):
        try:
            forecast, metrics, holdout = forecast_hhs_care(data, horizon=horizon)
            st.json(metrics)
            st.plotly_chart(px.line(forecast, x="forecast_step", y="hhs_care_forecast",
                                    title="Holt damped-trend baseline forecast"), use_container_width=True)
            st.dataframe(forecast, use_container_width=True)
        except Exception as exc:
            st.error(f"Forecast could not be fitted: {exc}")

st.divider()
st.caption(f"Showing {len(selected):,} observations from {selected.date.min():%d %b %Y} to {selected.date.max():%d %b %Y}.")
