import pandas as pd
import os

EVOLUTION_FILE = "data/business_evolution_10y.csv"
FUNDAMENTAL_FILE = "data/fundamental_core_dataset.csv"
SECTOR_FILE = "data/sector_strength_rank.csv"

OUT_FILE = "data/multibagger_candidates.csv"

def detect_multibaggers():

    if not os.path.exists(EVOLUTION_FILE):
        print("Business evolution file missing.")
        return

    evo = pd.read_csv(EVOLUTION_FILE)

    if os.path.exists(FUNDAMENTAL_FILE):
        fund = pd.read_csv(FUNDAMENTAL_FILE)
    else:
        fund = pd.DataFrame()

    if os.path.exists(SECTOR_FILE):
        sector = pd.read_csv(SECTOR_FILE)
    else:
        sector = pd.DataFrame()

    result = evo.copy()

    # basic multibagger conditions
    result["multibagger_score"] = 0

    result.loc[result["revenue_growth"] > 0, "multibagger_score"] += 1
    result.loc[result["profit_growth"] > 0, "multibagger_score"] += 1
    result.loc[result["debt_change"] <= 0, "multibagger_score"] += 1

    # keep strong candidates
    candidates = result[result["multibagger_score"] >= 2]

    candidates = candidates.sort_values(
        ["multibagger_score","profit_growth"],
        ascending=False
    )

    candidates.to_csv(OUT_FILE, index=False)

    print("MULTIBAGGER DETECTION COMPLETE")
    print("Candidates found:", len(candidates))
    print("Saved:", OUT_FILE)


# disabled_entry_point
    detect_multibaggers()
