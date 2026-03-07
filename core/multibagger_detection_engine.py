import pandas as pd
import os

DATA_FILE = "data/business_evolution_10y.csv"
OUT_FILE = "data/multibagger_candidates.csv"

def detect_multibaggers():

    if not os.path.exists(DATA_FILE):
        print("Business evolution data missing.")
        return

    df = pd.read_csv(DATA_FILE)

    if "revenue_growth" not in df.columns:
        print("Required columns missing.")
        return

    candidates = df[
        (df["revenue_growth"] > 0) &
        (df["profit_growth"] > 0)
    ]

    candidates = candidates.sort_values("revenue_growth", ascending=False)

    candidates.to_csv(OUT_FILE, index=False)

    print("MULTIBAGGER DETECTION COMPLETE")
    print("Candidates found:", len(candidates))
    print("Saved:", OUT_FILE)


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)


def run():
    print('Engine started:', __name__)
