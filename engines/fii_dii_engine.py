import csv

def load_fii_dii(filepath="data/fii_dii.csv"):
    flows = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            flows.append({
                "sector": row["sector"],
                "fii": float(row["fii"]),
                "dii": float(row["dii"])
            })
    return flows

def market_mood(flows):
    score = 0
    for f in flows:
        score += f["fii"] + f["dii"]

    if score > 0:
        return "RISK ON (BUY MODE)"
    elif score < 0:
        return "RISK OFF (DEFENSIVE MODE)"
    else:
        return "NEUTRAL"

# ✅ NEW UPGRADED FUNCTION
def get_money_flow(filepath="data/fii_dii.csv"):
    flows = load_fii_dii(filepath)

    sector_scores = {}
    total_flow = 0

    for f in flows:
        sector = f["sector"]
        flow = f["fii"] + f["dii"]
        sector_scores[sector] = flow
        total_flow += flow

    # sort sectors by money flow
    ranked = sorted(sector_scores.items(), key=lambda x: x[1], reverse=True)

    if total_flow > 0:
        mood = "RISK ON"
    elif total_flow < 0:
        mood = "RISK OFF"
    else:
        mood = "NEUTRAL"

    top_sector, top_flow = ranked[0]

    reason = f"Top sector flow: {top_sector} ({top_flow}), Total flow: {total_flow}"

    return {
        "mood": mood,
        "top_sector": top_sector,
        "top_flow": top_flow,
        "ranked_sectors": ranked,
        "reason": reason
    }
