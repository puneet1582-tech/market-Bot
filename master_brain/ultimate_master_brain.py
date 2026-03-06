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
    return "INVEST"

def fundamental_check(symbol):

    df = load_csv("quarterly_fundamentals_clean.csv")

    if len(df)==0:
        return "DATA_MISSING"

    df = df[df["symbol"]==symbol]

    if len(df)<4:
        return "WEAK"

    sales_growth = df["sales"].pct_change().mean()
    profit_growth = df["profit"].pct_change().mean()

    if sales_growth>0 and profit_growth>0:
        return "STRONG"

    return "AVERAGE"

def sector_check(symbol):

    stocks = load_csv("stocks.csv")

    if len(stocks)==0:
        return "UNKNOWN"

    df = stocks[stocks["symbol"]==symbol]

    if len(df)==0:
        return "UNKNOWN"

    return df.iloc[0]["sector"]

def institutional_check(sector):

    inst = load_csv("institutional_money_flow.csv")

    if len(inst)==0:
        return "UNKNOWN"

    df = inst[inst["sector"]==sector]

    if len(df)==0:
        return "UNKNOWN"

    strength = df.iloc[-1]["institutional_strength"]

    if strength>0:
        return "BUYING"

    return "SELLING"

def global_macro():

    p = DATA_DIR / "global/global_events.csv"

    if not p.exists():
        return "NEUTRAL"

    df = pd.read_csv(p)

    if len(df)==0:
        return "NEUTRAL"

    impact = str(df.iloc[-1]["impact"]).lower()

    if "positive" in impact:
        return "POSITIVE"

    if "negative" in impact:
        return "NEGATIVE"

    return "NEUTRAL"

def decision(fund, inst):

    if fund=="STRONG" and inst=="BUYING":
        return "INVEST"

    if fund in ["STRONG","AVERAGE"]:
        return "TRADE"

    return "AVOID"

def run_master_brain():

    stocks = load_csv("stocks.csv")

    if len(stocks)==0:
        print("NO STOCK DATA")
        return

    symbols = stocks["symbol"].tolist()

    macro = global_macro()

    results=[]

    for s in symbols[:200]:

        sector = sector_check(s)

        fund = fundamental_check(s)

        inst = institutional_check(sector)

        dec = decision(fund,inst)

        results.append({
            "stock":s,
            "sector":sector,
            "fundamental":fund,
            "institutional":inst,
            "decision":dec
        })

    output={
        "MARKET_MODE":market_mode(),
        "GLOBAL_MACRO":macro,
        "TOP_STOCK_ANALYSIS":results[:20]
    }

    print(json.dumps(output,indent=2))

if __name__ == "__main__":
    run_master_brain()
