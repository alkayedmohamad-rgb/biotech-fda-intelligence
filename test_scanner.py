import pandas as pd
from src.scanner import run_scan

def test_run_scan_returns_dataframe():
    # Network-backed integration test intentionally not run in CI by default.
    result = run_scan([])
    assert isinstance(result, pd.DataFrame)
    assert result.empty
