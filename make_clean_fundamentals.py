import pandas as pd

df = pd.read_csv("data/quarterly_fundamentals.csv")

# remove rows where both sales and profit are missing
df = df[~(df["sales"].isna() & df["profit"].isna())]

# convert quarter to datetime
df["quarter"] = pd.to_datetime(df["quarter"], errors="coerce")

# sort and keep last 12 quarters per stock
df = df.sort_values(["symbol", "quarter"], ascending=[True, False])
df = df.groupby("symbol").head(12)

df.to_csv("data/quarterly_fundamentals_clean.csv", index=False)

print("quarterly_fundamentals_clean.csv CREATED")
