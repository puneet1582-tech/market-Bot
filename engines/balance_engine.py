import yfinance as yf

def get_balance_cashflow(stock):
    try:
        t = yf.Ticker(stock + ".NS")
        bs = t.balance_sheet
        cf = t.cashflow

        if bs is None or cf is None or bs.empty or cf.empty:
            return None

        # Take last 3 years
        total_assets = bs.loc["Total Assets"].values[:3].tolist()
        total_debt = bs.loc["Total Debt"].values[:3].tolist()
        operating_cf = cf.loc["Total Cash From Operating Activities"].values[:3].tolist()

        return {
            "assets": list(reversed(total_assets)),
            "debt": list(reversed(total_debt)),
            "cashflow": list(reversed(operating_cf))
        }
    except:
        return None

def percent_change(old, new):
    if old == 0:
        return 0
    return round(((new - old) / old) * 100, 2)

def analyze_balance(stock):
    data = get_balance_cashflow(stock)
    if not data:
        return 0, ["No balance sheet / cash flow data"]

    assets = data["assets"]
    debt = data["debt"]
    cashflow = data["cashflow"]

    reasons = []
    score = 0

    assets_change = percent_change(assets[0], assets[-1])
    debt_change = percent_change(debt[0], debt[-1])
    cashflow_change = percent_change(cashflow[0], cashflow[-1])

    reasons.append(f"Assets change (3Y): {assets_change}%")
    reasons.append(f"Debt change (3Y): {debt_change}%")
    reasons.append(f"Operating Cash Flow change (3Y): {cashflow_change}%")

    if assets_change > 0:
        score += 1
    else:
        score -= 1

    if debt_change < 10:
        score += 1
    else:
        score -= 1

    if cashflow_change > 0:
        score += 1
    else:
        score -= 1

    return score, reasons
