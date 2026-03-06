import json
import pandas as pd
from business_evolution_engine import business_strength

def sector_check(symbol):

    df = pd.read_csv("data/stocks.csv")

    row = df[df["symbol"] == symbol]

    if len(row) == 0:
        return "UNKNOWN"

    return row.iloc[0]["sector"]

def institutional_check(sector):

    df = pd.read_csv("data/institutional_money_flow.csv")

    row = df[df["sector"] == sector]

    if len(row) == 0:
        return "UNKNOWN"

    strength = row.iloc[-1]["institutional_strength"]

    if strength > 0:
        return "BUYING"

    return "SELLING"

def decision(business, institutional):

    if business == "STRONG" and institutional == "BUYING":
        return "LONG TERM INVEST"

    if business in ["STRONG","AVERAGE"]:
        return "TRADE"

    return "AVOID"

def run_master_brain():

    stocks = pd.read_csv("data/stocks.csv")

    symbols = stocks["symbol"].tolist()

    results = []

    for s in symbols[:50]:

        sector = sector_check(s)

        business = business_strength(s)

        institutional = institutional_check(sector)

        final = decision(business,institutional)

        results.append({
            "stock": s,
            "sector": sector,
            "business": business,
            "institutional": institutional,
            "final_decision": final
        })

    output = {
        "BOT": "ULTIMATE BRAIN",
        "ANALYSIS": results[:20]
    }

    print(json.dumps(output,indent=2))

if __name__ == "__main__":
    run_master_brain()
