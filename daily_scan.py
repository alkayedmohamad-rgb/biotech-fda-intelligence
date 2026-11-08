from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.storage import load_watchlist
from src.scanner import run_scan
from datetime import date

out = Path(__file__).resolve().parents[1] / "reports"
out.mkdir(exist_ok=True)
df = run_scan(load_watchlist())
path = out / f"daily_scan_{date.today().isoformat()}.csv"
df.to_csv(path, index=False)
print(f"Saved {path}")
