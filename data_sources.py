import requests
import pandas as pd
from typing import Optional

HEADERS = {"User-Agent": "BiotechFDAIntelligence research contact: user@example.com"}

def fetch_yfinance(ticker: str, period: str = "1y") -> pd.DataFrame:
    try:
        import yfinance as yf
        hist = yf.Ticker(ticker).history(period=period, auto_adjust=True)
        if hist is None or hist.empty:
            return pd.DataFrame()
        hist = hist.reset_index()
        hist.columns = [str(c).lower().replace(" ", "_") for c in hist.columns]
        return hist
    except Exception:
        return pd.DataFrame()

def fetch_companyfacts(cik: str) -> dict:
    cik10 = str(cik).zfill(10)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json"
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}

def fetch_fda_approvals(limit: int = 100) -> pd.DataFrame:
    url = "https://api.fda.gov/drug/drugsfda.json"
    params = {"limit": min(max(int(limit), 1), 100), "sort": "submissions.submission_status_date:desc"}
    try:
        r = requests.get(url, params=params, timeout=25)
        r.raise_for_status()
        records = r.json().get("results", [])
        rows = []
        for item in records:
            products = item.get("products", [])
            sponsors = item.get("sponsor_name", "")
            for p in products[:3]:
                rows.append({
                    "application_number": item.get("application_number", ""),
                    "sponsor": sponsors,
                    "brand_name": p.get("brand_name", ""),
                    "active_ingredients": ", ".join(x.get("name", "") for x in p.get("active_ingredients", [])),
                    "dosage_form": p.get("dosage_form", ""),
                    "submission_status_date": (item.get("submissions") or [{}])[0].get("submission_status_date", "")
                })
        return pd.DataFrame(rows)
    except Exception as e:
        return pd.DataFrame([{"error": str(e)}])

def fetch_clinical_trials(query: str, page_size: int = 50) -> pd.DataFrame:
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {"query.term": query, "pageSize": min(max(int(page_size), 1), 100), "format": "json"}
    try:
        r = requests.get(url, params=params, timeout=25)
        r.raise_for_status()
        studies = r.json().get("studies", [])
        rows = []
        for s in studies:
            p = s.get("protocolSection", {})
            ident = p.get("identificationModule", {})
            status = p.get("statusModule", {})
            design = p.get("designModule", {})
            rows.append({
                "NCT": ident.get("nctId", ""),
                "title": ident.get("briefTitle", ""),
                "status": status.get("overallStatus", ""),
                "phase": ", ".join(design.get("phases", [])),
                "start_date": (status.get("startDateStruct") or {}).get("date", ""),
                "completion_date": (status.get("completionDateStruct") or {}).get("date", ""),
                "url": "https://clinicaltrials.gov/study/" + ident.get("nctId", "")
            })
        return pd.DataFrame(rows)
    except Exception as e:
        return pd.DataFrame([{"error": str(e)}])
