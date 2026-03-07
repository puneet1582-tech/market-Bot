import pandas as pd
import os

FUNDAMENTAL_FILE = "data/fundamental_core_dataset.csv"
SECTOR_FILE = "data/sector_strength_rank.csv"
MULTI_FILE = "data/multibagger_candidates.csv"

OUT_FILE = "data/top_opportunities.csv"


def detect_opportunities():

    if not os.path.exists(FUNDAMENTAL_FILE):
        print("Fundamental dataset missing.")
        return

    core = pd.read_csv(FUNDAMENTAL_FILE)

    sector = pd.read_csv(SECTOR_FILE) if os.path.exists(SECTOR_FILE) else pd.DataFrame()
    multi = pd.read_csv(MULTI_FILE) if os.path.exists(MULTI_FILE) else pd.DataFrame()

    if "symbol" not in core.columns:
        print("Symbol column missing.")
        return

    # sector merge
    if not sector.empty and "sector" in sector.columns:
        core = core.merge(sector, on="sector", how="left")

    # multibagger flag
    core["multibagger_flag"] = core["symbol"].isin(multi["symbol"]) if not multi.empty else False

    # simple opportunity score
    core["opportunity_score"] = core["multibagger_flag"].astype(int) * 2

    top = core.sort_values("opportunity_score", ascending=False)

    top = top[["symbol","sector","opportunity_score","multibagger_flag"]]

    top = top.drop_duplicates("symbol")

    top = top.head(20)

    top.to_csv(OUT_FILE, index=False)

    print("OPPORTUNITY ENGINE COMPLETE")
    print("Top stocks:", len(top))
    print("Saved:", OUT_FILE)



if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)


def run():
    print('Engine started:', __name__)
