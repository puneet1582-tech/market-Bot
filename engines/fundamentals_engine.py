import os
import pandas as pd

DATA_DIR = "data/fundamentals"
os.makedirs(DATA_DIR, exist_ok=True)

def load_universe():
    df = pd.read_csv("nse_universe.csv")
    return df

def create_fundamental_base():
    df = load_universe()

    df["revenue"] = None
    df["profit"] = None
    df["debt"] = None
    df["cash"] = None

    output = f"{DATA_DIR}/fundamentals.csv"
    df.to_csv(output, index=False)

    print("Fundamental base dataset created")

if __name__ == "__main__":
    create_fundamental_base()
