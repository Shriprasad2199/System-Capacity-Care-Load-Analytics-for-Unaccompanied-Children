# System Capacity & Care Load Analytics for Unaccompanied Children

## Project purpose
Analyse observed CBP custody, transfers into HHS, active HHS care and HHS discharges from January 2023 to December 2025. The project focuses on system load, operational flows, temporal patterns and transparent pressure indicators.

## Important interpretation limits
- The source contains 720 usable observations and 450 fully blank trailing rows.
- Reporting dates are irregular. Missing dates are not assumed to represent zero activity.
- Stock-flow identities do not consistently reconcile. Do not force balances or silently overwrite source values.
- No facility-level bed, staffing or licensed-capacity denominator is provided. The project measures system load and relative pressure, not actual facility occupancy or clinical capacity.
- Rolling windows are based on observations, not calendar days.
- Forecasts are a baseline over ordered reporting observations, not a validated daily operational forecast.

## Setup (macOS / VS Code)
From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m ipykernel install --user --name uac-capacity --display-name "Python (UAC Capacity)"
```

In VS Code, open the project folder, select `.venv` as the Python interpreter, then select the `Python (UAC Capacity)` notebook kernel.

## Run the pipeline
```bash
python -m src.run_pipeline
```

## Launch dashboard
```bash
streamlit run app/streamlit_app.py
```

## Suggested notebook order
1. `01_Data_Inspection.ipynb`
2. `02_Data_Cleaning.ipynb`
3. `03_Feature_Engineering.ipynb`
4. `04_Exploratory_Data_Analysis.ipynb`
5. `05_Temporal_Analysis.ipynb`
6. `06_Capacity_Stress_Analysis.ipynb`
7. `07_Forecasting.ipynb`

## KPI definitions
- Total system load = CBP custody + HHS care.
- HHS net flow = transfers to HHS - HHS discharges.
- System net flow = CBP intake - HHS discharges. Internal transfers cancel at combined-system level.
- HHS discharge offset ratio = HHS discharges / transfers to HHS, where transfers are positive.
- Care-load volatility index = 7-observation rolling standard deviation / rolling mean × 100.
- High system load = total system load at or above the full-sample 90th percentile. This is a relative statistical flag, not an official capacity threshold.
