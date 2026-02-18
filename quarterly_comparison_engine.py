import os
import pandas as pd
from datetime import datetime

DATA_DIR = "data/fundamentals"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

REPORT = os.path.join(OUTPUT_DIR, "quarterly_comparison_report.csv")

def run():
    frames = []
    for f in os.listdir(DATA_DIR) if os.path.exists(DATA_DIR) else []:
        if f.endswith(".csv"):
            try:
                df = pd.read_csv(os.path.join(DATA_DIR, f))
                df["SOURCE_FILE"] = f
                frames.append(df)
            except:
                pass

    if not frames:
        print("No fundamentals data available.")
        return

    combined = pd.concat(frames, ignore_index=True)
    combined["GENERATED_AT"] = datetime.now()
    combined.to_csv(REPORT, index=False)
    print("Quarterly comparison report saved:", REPORT)

if __name__ == "__main__":
    run()
