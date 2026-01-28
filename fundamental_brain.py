import yfinance as yf

stocks = ["TCS.NS", "HDFCBANK.NS", "ITC.NS"]

fundamental_data = {}

def to_crore(value):
    try:
        return round(value / 10000000, 2)  # 1 crore = 10,000,000
    except:
        return 0

for symbol in stocks:
    stock = yf.Ticker(symbol)
    info = stock.info

    name = symbol.replace(".NS", "")

    sector = info.get("sector", "NA")
    sales_raw = info.get("totalRevenue", 0)
    profit_raw = info.get("netIncomeToCommon", 0)
    debt_raw = info.get("totalDebt", 0)

    promoter = info.get("heldPercentInsiders", 0)
    fii = info.get("heldPercentInstitutions", 0)

    sales = to_crore(sales_raw)
    profit = to_crore(profit_raw)
    debt = to_crore(debt_raw)

    # Risk logic
    if debt == 0:
        risk = "LOW"
    elif debt > profit:
        risk = "HIGH"
    else:
        risk = "MEDIUM"

    fundamental_data[name] = {
        "sector": sector,
        "sales": f"{sales} Cr",
        "profit": f"{profit} Cr",
        "debt": f"{debt} Cr",
        "promoter_holding": round(promoter * 100, 2),
        "fii_holding": round(fii * 100, 2),
        "risk": risk
    }

# test print
print("REAL FUNDAMENTAL DATA (IN CRORES) READY")
for k, v in fundamental_data.items():
    print(k, v)
