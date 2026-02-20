import os
import pandas as pd
from datetime import datetime

DATA_DIR = "data/fundamentals"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

REPORT_FILE = os.path.join(OUTPUT_DIR, "top_opportunities.csv")

def load_all_fundamentals():
    frames = []
    if not os.path.exists(DATA_DIR):
        return pd.DataFrame()

    for f in os.listdir(DATA_DIR):
        if f.endswith(".csv"):
            try:
                df = pd.read_csv(os.path.join(DATA_DIR, f))
                frames.append(df)
            except:
                pass

    if frames:
        return pd.concat(frames, ignore_index=True)
    return pd.DataFrame()

def compute_scores(df):
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    if len(numeric_cols) == 0:
        return pd.DataFrame()

    df["SCORE"] = df[numeric_cols].sum(axis=1)
    return df.sort_values("SCORE", ascending=False)

def run():
    df = load_all_fundamentals()
    if df.empty:
        print("No fundamentals data available.")
        return

    scored = compute_scores(df)
    top = scored.head(20)
    top["GENERATED_AT"] = datetime.now()
    top.to_csv(REPORT_FILE, index=False)

    print("Top opportunity report saved:", REPORT_FILE)

# DISABLED ENTRY POINT
# if __name__ == "__main__":
    run()
