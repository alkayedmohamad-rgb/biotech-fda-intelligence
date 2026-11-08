import pandas as pd
import numpy as np
from data_sources import fetch_yfinance
def _safe_float(x):
    try:
        return float(x)
    except Exception:
        return np.nan

def analyze_ticker(ticker: str, lookback_days: int = 90) -> dict:
    hist = fetch_yfinance(ticker, period="1y")
    if hist.empty or "close" not in hist.columns:
        return {"ticker": ticker, "signal": "Insufficient data", "score": 0}
    hist = hist.dropna(subset=["close"]).tail(max(lookback_days, 20))
    close = hist["close"].astype(float)
    last = float(close.iloc[-1])
    ret_20 = float(close.pct_change(min(20, len(close)-1)).iloc[-1] * 100) if len(close) > 2 else np.nan
    ret_60 = float(close.pct_change(min(60, len(close)-1)).iloc[-1] * 100) if len(close) > 2 else np.nan
    vol = float(close.pct_change().dropna().std() * np.sqrt(252) * 100) if len(close) > 5 else np.nan
    avg_volume = float(hist["volume"].tail(20).mean()) if "volume" in hist.columns else np.nan
    score = 50
    if pd.notna(ret_20):
        score += max(-20, min(20, ret_20 * 0.5))
    if pd.notna(ret_60):
        score += max(-10, min(10, ret_60 * 0.2))
    score = int(max(0, min(100, round(score))))
    signal = "Bullish watch" if score >= 65 else ("Bearish watch" if score <= 35 else "Neutral")
    return {
        "ticker": ticker, "price": round(last, 2), "return_20d_%": round(ret_20, 2) if pd.notna(ret_20) else None,
        "return_60d_%": round(ret_60, 2) if pd.notna(ret_60) else None,
        "annualized_volatility_%": round(vol, 2) if pd.notna(vol) else None,
        "avg_volume_20d": int(avg_volume) if pd.notna(avg_volume) else None,
        "momentum_score_0_100": score, "signal": signal,
        "data_note": "Price/momentum only; FDA catalyst not verified"
    }

def run_scan(tickers, lookback_days: int = 90) -> pd.DataFrame:
    rows = [analyze_ticker(t, lookback_days) for t in tickers]
    return pd.DataFrame(rows)
