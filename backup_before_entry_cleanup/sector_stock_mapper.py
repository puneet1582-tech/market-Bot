import pandas as pd
import os

OUTPUT = "output/sector_stock_map.csv"
os.makedirs("output", exist_ok=True)

data = {
    "Sector": ["Banking", "IT", "Energy"],
    "Example Stocks": ["HDFCBANK, ICICIBANK", "TCS, INFY", "RELIANCE, ONGC"]
}

pd.DataFrame(data).to_csv(OUTPUT, index=False)
print("Sector mapping created:", OUTPUT)
