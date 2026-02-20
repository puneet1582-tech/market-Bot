import pandas as pd

STOCKS_PATH = "data/stocks.csv"
MAP_PATH = "data/sector_map.csv"

df_stocks = pd.read_csv(STOCKS_PATH)
df_map = pd.read_csv(MAP_PATH)

df_stocks["company"] = df_stocks["company"].astype(str).str.upper()

for i, row in df_stocks.iterrows():
    name = row["company"]
    sector_found = False

    for _, m in df_map.iterrows():
        if m["keyword"] in name:
            df_stocks.at[i, "sector"] = m["sector"]
            sector_found = True
            break

    if not sector_found:
        df_stocks.at[i, "sector"] = "Smallcap"

df_stocks.to_csv(STOCKS_PATH, index=False)
print("SECTOR CLASSIFICATION DONE")
