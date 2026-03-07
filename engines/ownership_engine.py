import pandas as pd
import os

UNIVERSE_FILE = "nse_universe.csv"
OUTPUT_FILE = "data/fundamentals/ownership_data.csv"

def create_ownership_base():

    if not os.path.exists(UNIVERSE_FILE):
        print("Universe file missing")
        return

    df = pd.read_csv(UNIVERSE_FILE)

    df["promoter_holding"] = None
    df["fii_holding"] = None
    df["dii_holding"] = None
    df["public_holding"] = None

    os.makedirs("data/fundamentals", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("Ownership base dataset created")


if __name__ == "__main__":
    create_ownership_base()
