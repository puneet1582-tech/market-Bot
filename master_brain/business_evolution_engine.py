import pandas as pd

def business_strength(symbol):

    try:
        df = pd.read_csv("data/quarterly_fundamentals_clean.csv")
    except:
        return "DATA_MISSING"

    df = df[df["symbol"] == symbol]

    if len(df) < 4:
        return "WEAK"

    sales_trend = df["sales"].pct_change().mean()
    profit_trend = df["profit"].pct_change().mean()
    cashflow_trend = df["cashflow"].pct_change().mean()
    debt_trend = df["debt"].pct_change().mean()

    score = 0

    if sales_trend > 0:
        score += 1

    if profit_trend > 0:
        score += 1

    if cashflow_trend > 0:
        score += 1

    if debt_trend < 0:
        score += 1

    if score >= 3:
        return "STRONG"

    if score == 2:
        return "AVERAGE"

    return "WEAK"
