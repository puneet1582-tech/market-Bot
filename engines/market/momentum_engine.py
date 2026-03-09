import pandas as pd

INPUT_FILE = "data/processed/tradable_universe.csv"
OUTPUT_FILE = "data/processed/momentum_stocks.csv"

def calculate_momentum():

    df = pd.read_csv(INPUT_FILE)

    df["range"] = df["high"] - df["low"]
    df["momentum"] = (df["close"] - df["open"]) / df["open"] * 100

    df = df[df["momentum"] > 1]

    df = df.sort_values(by="momentum", ascending=False)

    df.to_csv(OUTPUT_FILE, index=False)

    print("Momentum analysis complete")
    print(f"Momentum stocks found: {len(df)}")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    calculate_momentum()
