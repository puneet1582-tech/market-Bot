import yfinance as yf
import pandas as pd

stocks_df = pd.read_csv("data/stocks.csv")

rows = []

# सिर्फ पहले 10 stocks पर test (slow न हो)
symbols = stocks_df["symbol"].head(10).tolist()

for sym in symbols:
    ticker = sym + ".NS"
    print("Fetching:", ticker)
    t = yf.Ticker(ticker)

    try:
        fin = t.quarterly_financials
        bs = t.quarterly_balance_sheet
        cf = t.quarterly_cashflow

        if fin.empty:
            print("No financials:", ticker)
            continue

        for col in fin.columns:
            rows.append({
                "symbol": sym,
                "quarter": col.strftime("%Y-%m"),
                "sales": fin.loc["Total Revenue", col] if "Total Revenue" in fin.index else None,
                "profit": fin.loc["Net Income", col] if "Net Income" in fin.index else None,
                "debt": bs.loc["Total Debt", col] if (bs is not None and "Total Debt" in bs.index) else None,
                "cashflow": cf.loc["Total Cash From Operating Activities", col] if (cf is not None and "Total Cash From Operating Activities" in cf.index) else None
            })
    except Exception as e:
        print("Failed:", ticker, e)

df = pd.DataFrame(rows)
df.to_csv("data/quarterly_fundamentals.csv", index=False)

print("SMART FUNDAMENTALS UPDATED")
