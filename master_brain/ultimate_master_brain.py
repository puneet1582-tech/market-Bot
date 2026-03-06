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

def find_column(df, options):
    for c in options:
        if c in df.columns:
            return c
    return None

def market_mode():
    vol = load_csv("nifty_volatility.csv")
    if len(vol)==0:
        return "NORMAL"

    col = find_column(vol,["volatility","value","vix"])

    if col is None:
        return "NORMAL"

    v = float(vol.iloc[-1][col])

    if v>20:
        return "TRADE"

    return "INVEST"

def fundamental_check(symbol):

    q = load_csv("quarterly_fundamentals_clean.csv")

    if len(q)==0:
        return "DATA_MISSING"

    sym_col = find_column(q,["symbol","ticker","stock"])

    if sym_col is None:
        return "DATA_MISSING"

    df = q[q[sym_col]==symbol]

    if len(df)<4:
        return "WEAK"

    rev_col = find_column(df,["revenue","sales"])
    prof_col = find_column(df,["net_profit","profit"])

    if rev_col is None or prof_col is None:
        return "AVERAGE"

    rev_growth = df[rev_col].pct_change().mean()
    profit_growth = df[prof_col].pct_change().mean()

    if rev_growth>0 and profit_growth>0:
        return "STRONG"

    return "AVERAGE"

def institutional_check(symbol):

    inst = load_csv("institutional_money_flow.csv")

    if len(inst)==0:
        return "UNKNOWN"

    sym_col = find_column(inst,["symbol","stock","ticker"])
    flow_col = find_column(inst,["flow","money_flow","net_flow"])

    if sym_col is None or flow_col is None:
        return "UNKNOWN"

    df = inst[inst[sym_col]==symbol]

    if len(df)==0:
        return "UNKNOWN"

    flow = float(df.iloc[-1][flow_col])

    if flow>0:
        return "BUYING"

    return "SELLING"

def sector_check(symbol):

    sec = load_csv("sector_map.csv")

    if len(sec)==0:
        return "UNKNOWN"

    sym_col = find_column(sec,["symbol","stock","ticker"])
    sec_col = find_column(sec,["sector","industry"])

    if sym_col is None or sec_col is None:
        return "UNKNOWN"

    df = sec[sec[sym_col]==symbol]

    if len(df)==0:
        return "UNKNOWN"

    return df.iloc[0][sec_col]

def global_macro():

    g = DATA_DIR / "global/global_events.csv"

    if not g.exists():
        return "NEUTRAL"

    df = pd.read_csv(g)

    if len(df)==0:
        return "NEUTRAL"

    col = find_column(df,["impact","signal"])

    if col is None:
        return "NEUTRAL"

    impact = str(df.iloc[-1][col]).lower()

    if "positive" in impact:
        return "POSITIVE"

    if "negative" in impact:
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

    sym_col = find_column(universe,["symbol","stock","ticker"])

    if sym_col is None:
        print("SYMBOL COLUMN NOT FOUND")
        return

    symbols = universe[sym_col].tolist()

    market = market_mode()
    macro = global_macro()

    result=[]

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

    output={
        "MARKET_MODE":market,
        "GLOBAL_MACRO":macro,
        "TOP_STOCK_ANALYSIS":result[:20]
    }

    print(json.dumps(output,indent=2))

if __name__ == "__main__":
    run_master_brain()
