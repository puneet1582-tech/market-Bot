import pandas as pd

INPUT_FILE = "data/processed/momentum_stocks.csv"
OUTPUT_FILE = "data/processed/top_opportunities.csv"

def generate_opportunities():

    df = pd.read_csv(INPUT_FILE)

    df["score"] = (df["momentum"] * 0.6) + (df["volume"] * 0.00001)

    df = df.sort_values(by="score", ascending=False)

    top20 = df.head(20)

    top20.to_csv(OUTPUT_FILE, index=False)

    print("Top Opportunity Engine Complete")
    print(f"Top stocks generated: {len(top20)}")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_opportunities()
