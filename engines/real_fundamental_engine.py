import yfinance as yf

def get_quarterly_fundamentals(stock):
    try:
        ticker = yf.Ticker(stock + ".NS")
        fin = ticker.quarterly_financials

        if fin is None or fin.empty:
            return None

        sales = fin.loc["Total Revenue"].values.tolist()
        profit = fin.loc["Net Income"].values.tolist()

        return {
            "sales": list(reversed(sales)),   # oldest → newest
            "profit": list(reversed(profit))
        }
    except:
        return None

def percent_change(old, new):
    if old == 0:
        return 0
    return round(((new - old) / old) * 100, 2)

def analyze_real_fundamental(stock):
    data = get_quarterly_fundamentals(stock)
    if not data:
        return 0, ["No real quarterly data found"]

    sales = data["sales"]
    profit = data["profit"]

    reasons = []
    score = 0

    sales_change = percent_change(sales[0], sales[-1])
    profit_change = percent_change(profit[0], profit[-1])

    reasons.append(f"Quarterly Sales change: {sales_change}%")
    reasons.append(f"Quarterly Profit change: {profit_change}%")

    if sales_change > 10:
        score += 1
    else:
        score -= 1

    if profit_change > 10:
        score += 1
    else:
        score -= 1

    return score, reasons
