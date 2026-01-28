import pandas as pd

df = pd.read_csv("data/EQUITY_L.csv")

# Clean column names (remove extra spaces)
df.columns = [c.strip().upper() for c in df.columns]

# Select correct columns
stocks = df[["SYMBOL", "NAME OF COMPANY", "ISIN NUMBER"]].copy()

stocks.columns = ["symbol", "company", "isin"]

stocks["sector"] = "UNKNOWN"

stocks.to_csv("data/stocks.csv", index=False)

print("NSE STOCK UNIVERSE UPDATED")
print("Total stocks:", len(stocks))
