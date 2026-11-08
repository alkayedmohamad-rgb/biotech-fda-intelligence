from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
WATCHLIST = DATA / "watchlist.csv"
CATALYSTS = DATA / "catalysts.csv"

DEFAULT_TICKERS = ["XBI", "IBB", "MRNA", "BNTX", "REGN", "VRTX", "CRSP", "NTLA", "SANA", "IOVA"]

def load_watchlist():
    if not WATCHLIST.exists():
        save_watchlist(DEFAULT_TICKERS)
    try:
        return pd.read_csv(WATCHLIST)["ticker"].dropna().astype(str).tolist()
    except Exception:
        return DEFAULT_TICKERS

def save_watchlist(tickers):
    pd.DataFrame({"ticker": sorted(set(tickers))}).to_csv(WATCHLIST, index=False)

def load_catalysts():
    if CATALYSTS.exists():
        return pd.read_csv(CATALYSTS)
    return pd.DataFrame(columns=["ticker", "drug", "event_type", "event_date", "date_status", "source_url", "notes"])
