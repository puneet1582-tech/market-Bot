import pandas as pd
import os

DATA_DIR = "data"

Q_FILE = f"{DATA_DIR}/quarterly_fundamentals_clean.csv"
A_FILE = f"{DATA_DIR}/annual_10y/annual_fundamentals_10y.csv"
P_FILE = f"{DATA_DIR}/promoter_holdings.csv"
F_FILE = f"{DATA_DIR}/fii_dii.csv"

OUT_FILE = f"{DATA_DIR}/fundamental_core_dataset.csv"


def load_safe(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame()


def build_fundamental_core():

    q = load_safe(Q_FILE)
    a = load_safe(A_FILE)
    p = load_safe(P_FILE)
    f = load_safe(F_FILE)

    frames = []

    if not q.empty:
        q["source"] = "quarterly"
        frames.append(q)

    if not a.empty:
        a["source"] = "annual"
        frames.append(a)

    core = pd.concat(frames, ignore_index=True)

    if not p.empty:
        core = core.merge(p, on="symbol", how="left")

    if not f.empty:
        core = core.merge(f, on="symbol", how="left")

    core.to_csv(OUT_FILE, index=False)

    print("FUNDAMENTAL CORE DATASET BUILT")
    print("Rows:", len(core))
    print("Saved:", OUT_FILE)


if __name__ == "__main__":
    build_fundamental_core()
