import pandas as pd
import os

DATA_DIR = "data"

Q_FILE = f"{DATA_DIR}/quarterly_fundamentals_clean.csv"
A_FILE = f"{DATA_DIR}/annual_10y/annual_fundamentals_10y.csv"
P_FILE = f"{DATA_DIR}/promoter_holdings.csv"
F_FILE = f"{DATA_DIR}/fii_dii.csv"
SECTOR_FILE = f"{DATA_DIR}/sector_final_authority.csv"

OUT_FILE = f"{DATA_DIR}/fundamental_core_dataset.csv"


def load_safe(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def build_fundamental_core():

    q = load_safe(Q_FILE)
    a = load_safe(A_FILE)
    p = load_safe(P_FILE)
    f = load_safe(F_FILE)
    s = load_safe(SECTOR_FILE)

    frames = []

    if not q.empty:
        q["source"] = "quarterly"
        frames.append(q)

    if not a.empty:
        a["source"] = "annual"
        frames.append(a)

    if len(frames) == 0:
        print("No fundamental data found.")
        return

    core = pd.concat(frames, ignore_index=True)

    # merge promoter data
    if not p.empty and "symbol" in p.columns:
        core = core.merge(p, on="symbol", how="left")

    # merge sector
    if not s.empty and "symbol" in s.columns:
        core = core.merge(s[["symbol","sector"]], on="symbol", how="left")

    # merge fii/dii by sector
    if not f.empty and "sector" in f.columns:
        core = core.merge(f, on="sector", how="left")

    core.to_csv(OUT_FILE, index=False)

    print("FUNDAMENTAL CORE DATASET BUILT")
    print("Rows:", len(core))
    print("Saved:", OUT_FILE)


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
