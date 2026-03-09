import pandas as pd
import os

INPUT_FILE = "data/processed/market_prices.csv"
OUTPUT_FILE = "data/processed/market_mode.csv"

def run():

    df = pd.read_csv(INPUT_FILE)

    # convert to numeric safely
    df["close"] = (
        df["close"]
        .astype(str)
        .str.replace(",", "")
    )

    df["volume"] = (
        df["volume"]
        .astype(str)
        .str.replace(",", "")
    )

    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce")

    df = df.dropna(subset=["close","volume"])

    avg_close = df["close"].mean()
    avg_volume = df["volume"].mean()

    high_movers = df[df["close"] > avg_close]

    participation = len(high_movers) / len(df)

    if participation > 0.6:
        mode = "BULL"
    elif participation > 0.4:
        mode = "SIDEWAYS"
    else:
        mode = "RISK"

    result = pd.DataFrame([{
        "market_mode": mode,
        "avg_price": avg_close,
        "avg_volume": avg_volume,
        "participation": participation
    }])

    os.makedirs("data/processed", exist_ok=True)

    result.to_csv(OUTPUT_FILE, index=False)

    print("Market mode detected")
    print(result)


if __name__ == "__main__":
    run()
