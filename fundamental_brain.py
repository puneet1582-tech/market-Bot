import yfinance as yf

stocks = ["TCS.NS", "HDFCBANK.NS", "ITC.NS"]

fundamental_data = {}

for symbol in stocks:
    stock = yf.Ticker(symbol)
    info = stock.info

    name = symbol.replace(".NS", "")

    sector = info.get("sector", "NA")
    sales = info.get("totalRevenue", 0)
    profit = info.get("netIncomeToCommon", 0)
    debt = info.get("totalDebt", 0)

    promoter = info.get("heldPercentInsiders", 0)
    fii = info.get("heldPercentInstitutions", 0)

    # Risk logic from debt + profit
    if debt == 0:
        risk = "LOW"
    elif debt > profit:
        risk = "HIGH"
    else:
        risk = "MEDIUM"

    fundamental_data[name] = {
        "sector": sector,
        "sales": sales,
        "profit": profit,
        "debt": debt,
        "promoter_holding": round(promoter * 100, 2),
        "fii_holding": round(fii * 100, 2),
        "risk": risk
    }

# test print
print("REAL FUNDAMENTAL DATA READY")
for k, v in fundamental_data.items():
    print(k, v)
