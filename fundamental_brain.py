import yfinance as yf

# NIFTY50 stocks list
stocks = [
    "ADANIENT.NS","ADANIPORTS.NS","APOLLOHOSP.NS","ASIANPAINT.NS","AXISBANK.NS",
    "BAJAJ-AUTO.NS","BAJFINANCE.NS","BAJAJFINSV.NS","BHARTIARTL.NS","BPCL.NS",
    "BRITANNIA.NS","CIPLA.NS","COALINDIA.NS","DIVISLAB.NS","DRREDDY.NS",
    "EICHERMOT.NS","GRASIM.NS","HCLTECH.NS","HDFCBANK.NS","HDFCLIFE.NS",
    "HEROMOTOCO.NS","HINDALCO.NS","HINDUNILVR.NS","ICICIBANK.NS","ITC.NS",
    "INDUSINDBK.NS","INFY.NS","JSWSTEEL.NS","KOTAKBANK.NS","LT.NS",
    "LTIM.NS","MARUTI.NS","NESTLEIND.NS","NTPC.NS","ONGC.NS",
    "POWERGRID.NS","RELIANCE.NS","SBILIFE.NS","SBIN.NS","SUNPHARMA.NS",
    "TATACONSUM.NS","TATAMOTORS.NS","TATASTEEL.NS","TCS.NS","TECHM.NS",
    "TITAN.NS","ULTRACEMCO.NS","UPL.NS","WIPRO.NS"
]

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

print("REAL FUNDAMENTAL DATA (NIFTY50, IN CRORES) READY")
for k, v in fundamental_data.items():
    print(k, v)
