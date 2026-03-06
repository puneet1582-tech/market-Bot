import pandas as pd
import requests
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_nse_universe():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    df = pd.read_csv(pd.compat.StringIO(r.text))
    df = df.rename(columns={
        "SYMBOL": "symbol",
        "NAME OF COMPANY": "company",
        "ISIN NUMBER": "isin"
    })[["symbol","company","isin"]]
    df["sector"] = "UNKNOWN"
    df.to_csv(DATA_DIR / "stocks.csv", index=False)
    print("NSE universe saved:", len(df))

def fetch_screener_fundamentals():
    base = "https://www.screener.in/api/company/"
    stocks = pd.read_csv(DATA_DIR / "stocks.csv")
    rows = []

    for sym in stocks["symbol"][:200]:
        try:
            url = f"{base}{sym}/"
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code!=200:
                continue
            data = r.json()
            q = data.get("quarterly_results", [])
            for item in q:
                rows.append({
                    "symbol": sym,
                    "quarter": item.get("quarter"),
                    "sales": item.get("sales"),
                    "profit": item.get("net_profit"),
                    "eps": item.get("eps"),
                    "debt": item.get("debt"),
                    "cashflow": item.get("cash_flow")
                })
        except:
            continue

    df = pd.DataFrame(rows)
    df.to_csv(DATA_DIR / "quarterly_fundamentals_clean.csv", index=False)
    print("Quarterly fundamentals saved:", len(df))

def build_sector_map():
    stocks = pd.read_csv(DATA_DIR / "stocks.csv")

    keywords = {
        "BANK": ["BANK","FINANCE","NBFC"],
        "IT": ["TECH","SOFT","INFOTECH"],
        "PHARMA": ["PHARMA","DRUG"],
        "AUTO": ["AUTO","MOTOR"],
        "METAL": ["STEEL","METAL"],
        "INFRA": ["INFRA","ENGINEERING"],
    }

    sectors = []
    for _,row in stocks.iterrows():
        name = str(row["company"]).upper()
        sector = "OTHER"
        for s,keys in keywords.items():
            if any(k in name for k in keys):
                sector = s
                break
        sectors.append(sector)

    stocks["sector"] = sectors
    stocks.to_csv(DATA_DIR / "stocks.csv", index=False)

    print("Sector mapping complete")

def institutional_template():
    df = pd.DataFrame(columns=["sector","fii","dii","institutional_strength"])
    df.to_csv(DATA_DIR / "institutional_money_flow.csv", index=False)
    print("Institutional template created")

def run():
    print("REAL DATA PIPELINE START")

    fetch_nse_universe()
    build_sector_map()
    fetch_screener_fundamentals()
    institutional_template()

    print("REAL DATA PIPELINE COMPLETE")

if __name__ == "__main__":
    run()
