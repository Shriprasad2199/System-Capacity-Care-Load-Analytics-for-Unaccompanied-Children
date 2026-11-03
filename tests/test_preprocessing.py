import pandas as pd
from src.preprocessing import clean_data

def test_clean_data_removes_blank_rows_and_sorts():
    raw = pd.DataFrame({
        "Date": ["January 2, 2024", None, "January 1, 2024"],
        "Children apprehended and placed in CBP custody*": ["2", None, "1"],
        "Children in CBP custody": ["3", None, "2"],
        "Children transferred out of CBP custody": ["1", None, "1"],
        "Children in HHS Care": ["1,000", None, "900"],
        "Children discharged from HHS Care": ["1", None, "0"],
    })
    clean = clean_data(raw)
    assert len(clean) == 2
    assert clean.date.is_monotonic_increasing
    assert clean.hhs_care.iloc[0] == 900
