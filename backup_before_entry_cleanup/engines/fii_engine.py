import csv

def load_fii_dii_data(filepath="data/fii_dii.csv"):
    data = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["fii"] = float(row["fii"])
            row["dii"] = float(row["dii"])
            data.append(row)
    return data

def fii_dii_signal(sector, data):
    fii_total = 0
    dii_total = 0

    for row in data:
        if row["sector"] == sector:
            fii_total += row["fii"]
            dii_total += row["dii"]

    reasons = []
    score = 0

    reasons.append(f"FII flow: {fii_total} crore")
    reasons.append(f"DII flow: {dii_total} crore")

    if fii_total > 0:
        score += 1
        reasons.append("FII buying")
    else:
        score -= 1
        reasons.append("FII selling")

    if dii_total > 0:
        score += 1
        reasons.append("DII buying")
    else:
        score -= 1
        reasons.append("DII selling")

    return score, reasons
