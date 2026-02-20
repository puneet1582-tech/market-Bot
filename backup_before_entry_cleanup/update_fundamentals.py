import yfinance as yf
import pandas as pd

stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]

rows = []

for s in stocks:
    t = yf.Ticker(s)
    try:
        fin = t.quarterly_financials
        bs = t.quarterly_balance_sheet
        cf = t.quarterly_cashflow

        for col in fin.columns:
            rows.append({
                "symbol": s.replace(".NS",""),
                "quarter": col.strftime("%Y-%m"),
                "sales": fin.loc["Total Revenue", col] if "Total Revenue" in fin.index else None,
                "profit": fin.loc["Net Income", col] if "Net Income" in fin.index else None,
                "eps": t.info.get("trailingEps"),
                "debt": bs.loc["Total Debt", col] if "Total Debt" in bs.index else None,
                "cashflow": cf.loc["Total Cash From Operating Activities", col] if "Total Cash From Operating Activities" in cf.index else None
            })
    except:
        print("Failed:", s)

df = pd.DataFrame(rows)
df.to_csv("data/quarterly_fundamentals.csv", index=False)

print("FUNDAMENTALS UPDATED")
