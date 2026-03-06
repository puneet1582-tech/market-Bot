import pandas as pd
import json
from pathlib import Path

DATA = Path("data")

def load(name):
    p = DATA / name
    if p.exists():
        try:
            return pd.read_csv(p)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def market_mode():
    try:
        vix = load("nifty_volatility.csv")
        if len(vix)==0:
            return "NORMAL"
        last=vix.iloc[-1]["volatility"]
        if last>25:
            return "DEFENSIVE"
        if last<15:
            return "INVEST"
        return "TRADE"
    except:
        return "NORMAL"

def sector_of(symbol,stocks):
    try:
        row=stocks[stocks["symbol"]==symbol]
        if len(row)==0:
            return "UNKNOWN"
        s=row.iloc[0]["sector"]
        if pd.isna(s) or s=="UNKNOWN":
            return "OTHER"
        return s
    except:
        return "OTHER"

def business_strength(symbol):
    df=load("quarterly_fundamentals_clean.csv")
    df=df[df["symbol"]==symbol]

    if len(df)<4:
        return "DATA_MISSING"

    sales=df["sales"].pct_change().mean()
    profit=df["profit"].pct_change().mean()
    cash=df["cashflow"].pct_change().mean()
    debt=df["debt"].pct_change().mean()

    score=0
    if sales>0: score+=1
    if profit>0: score+=1
    if cash>0: score+=1
    if debt<0: score+=1

    if score>=3:
        return "STRONG"
    if score==2:
        return "AVERAGE"
    return "WEAK"

def institutional_strength(sector):
    inst=load("institutional_money_flow.csv")
    df=inst[inst["sector"]==sector]

    if len(df)==0:
        return "UNKNOWN"

    v=df.iloc[0]["institutional_strength"]

    if v>0:
        return "BUYING"
    if v<0:
        return "SELLING"
    return "NEUTRAL"

def sector_strength(sector):
    s=load("sector_strength_rank.csv")
    df=s[s["sector"]==sector]

    if len(df)==0:
        return "NORMAL"

    r=df.iloc[0]["strength"]

    if r>0.6:
        return "STRONG"
    if r<0.3:
        return "WEAK"
    return "NORMAL"

def final_decision(business,inst,sector):

    if business=="STRONG" and inst=="BUYING":
        return "LONG_TERM_INVEST"

    if business in ["STRONG","AVERAGE"] and sector=="STRONG":
        return "SWING_TRADE"

    if business=="WEAK":
        return "AVOID"

    return "WATCH"

def run():

    stocks=load("stocks.csv")
    symbols=list(stocks["symbol"])[:20]

    mode=market_mode()

    output=[]

    for s in symbols:

        sector=sector_of(s,stocks)
        business=business_strength(s)
        inst=institutional_strength(sector)
        sec_strength=sector_strength(sector)

        decision=final_decision(business,inst,sec_strength)

        reason=f"{business} business + {inst} institutional flow + {sec_strength} sector"

        output.append({
            "stock":s,
            "sector":sector,
            "business":business,
            "institutional":inst,
            "sector_strength":sec_strength,
            "decision":decision,
            "reason":reason
        })

    result={
        "BOT":"ULTIMATE_BRAIN",
        "MARKET_MODE":mode,
        "ANALYSIS":output
    }

    print(json.dumps(result,indent=2))

if __name__=="__main__":
    run()
