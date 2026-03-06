import json
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

def load_csv(name):
    p = DATA_DIR / name
    if p.exists():
        try:
            return pd.read_csv(p)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def market_mode():
    try:
        vol = load_csv("nifty_volatility.csv")
        if len(vol)==0:
            return "NORMAL"
        v = vol.iloc[-1].to_dict()
        if float(list(v.values())[1]) > 20:
            return "TRADE"
        return "INVEST"
    except:
        return "NORMAL"

def fundamental_check(symbol):

    q = load_csv("quarterly_fundamentals_clean.csv")
    if len(q)==0:
        return "DATA_MISSING"

    df = q[q["symbol"]==symbol]

    if len(df) < 4:
        return "WEAK"

    rev_growth = df["revenue"].pct_change().mean()
    profit_growth = df["net_profit"].pct_change().mean()

    if rev_growth>0 and profit_growth>0:
        return "STRONG"

    return "AVERAGE"

def institutional_check(symbol):

    inst = load_csv("institutional_money_flow.csv")

    if len(inst)==0:
        return "UNKNOWN"

    df = inst[inst["symbol"]==symbol]

    if len(df)==0:
        return "UNKNOWN"

    flow = df.iloc[-1]["flow"]

    if flow>0:
        return "BUYING"

    return "SELLING"

def sector_check(symbol):

    sec = load_csv("sector_map.csv")

    if len(sec)==0:
        return "UNKNOWN"

    df = sec[sec["symbol"]==symbol]

    if len(df)==0:
        return "UNKNOWN"

    return df.iloc[0]["sector"]

def global_macro():

    g = DATA_DIR / "global/global_events.csv"

    if not g.exists():
        return "NEUTRAL"

    df = pd.read_csv(g)

    if len(df)==0:
        return "NEUTRAL"

    impact = df.iloc[-1]["impact"]

    if impact=="positive":
        return "POSITIVE"

    if impact=="negative":
        return "NEGATIVE"

    return "NEUTRAL"

def decision(symbol):

    fund = fundamental_check(symbol)
    inst = institutional_check(symbol)

    if fund=="STRONG" and inst=="BUYING":
        return "INVEST"

    if fund=="AVERAGE":
        return "TRADE"

    return "AVOID"

def run_master_brain():

    universe = load_csv("stocks.csv")

    if len(universe)==0:
        print("NO STOCK DATA")
        return

    symbols = universe["symbol"].tolist()

    market = market_mode()
    macro = global_macro()

    result = []

    for s in symbols[:200]:

        fund = fundamental_check(s)
        inst = institutional_check(s)
        sector = sector_check(s)
        dec = decision(s)

        result.append({
            "stock":s,
            "sector":sector,
            "fundamental":fund,
            "institutional":inst,
            "decision":dec
        })

    output = {
        "MARKET_MODE":market,
        "GLOBAL_MACRO":macro,
        "STOCK_ANALYSIS":result[:20]
    }

    print(json.dumps(output,indent=2))

if __name__ == "__main__":
    run_master_brain()
