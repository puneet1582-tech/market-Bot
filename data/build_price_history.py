import pandas as pd
import yfinance as yf

stocks = pd.read_csv("data/stocks.csv")

rows = []

for sym in stocks["symbol"][:300]:

    ticker = sym + ".NS"

    try:

        df = yf.download(ticker, period="5y", progress=False)

        if len(df)==0:
            continue

        for d,p in df["Close"].items():

            rows.append({
                "symbol": sym,
                "date": str(d.date()),
                "price": float(p)
            })

    except:
        continue

price = pd.DataFrame(rows)

price.to_csv("data/price_history.csv", index=False)

print("Price history created:", len(price))
