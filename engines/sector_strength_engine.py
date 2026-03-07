import pandas as pd

PRICE_FILE = "data/prices/historical_prices.csv"

SECTOR_MAP = {
    "IT": ["TCS","INFY","HCLTECH","WIPRO"],
    "BANK": ["HDFCBANK","ICICIBANK","SBIN","KOTAKBANK"],
    "AUTO": ["MARUTI","TATAMOTORS","M&M"],
    "METAL": ["TATASTEEL","JSWSTEEL","HINDALCO"],
    "DEFENCE": ["HAL","BEL","BDL"],
}

def sector_strength():

    try:
        df = pd.read_csv(PRICE_FILE)
    except:
        return {}

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    df = df.groupby("symbol").tail(2)

    df["ret"] = df.groupby("symbol")["price"].pct_change()

    df = df.dropna()

    strength = {}

    for sector, stocks in SECTOR_MAP.items():

        sub = df[df["symbol"].isin(stocks)]

        if len(sub) == 0:
            continue

        strength[sector] = sub["ret"].mean()

    return strength


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
