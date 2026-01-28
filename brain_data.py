stocks = [
    "RELIANCE",
    "TCS",
    "INFY",
    "HDFCBANK",
    "ICICIBANK",
    "SBIN",
    "LT",
    "ITC",
    "AXISBANK",
    "BAJFINANCE",
    "BHARTIARTL",
    "MARUTI",
    "HINDUNILVR",
    "SUNPHARMA",
    "NTPC",
    "POWERGRID",
    "ONGC",
    "TITAN",
    "ADANIENT",
    "WIPRO"
]

sectors = {
    "IT": ["TCS", "INFY", "WIPRO"],
    "BANKING": ["HDFCBANK", "ICICIBANK", "SBIN", "AXISBANK"],
    "ENERGY": ["RELIANCE", "ONGC"],
    "FMCG": ["ITC", "HINDUNILVR"],
    "AUTO": ["MARUTI"],
    "PHARMA": ["SUNPHARMA"],
    "METAL": ["ADANIENT"],
    "POWER": ["NTPC", "POWERGRID"],
    "OTHERS": ["LT", "TITAN", "BHARTIARTL", "BAJFINANCE"]
}

print("TOTAL STOCKS:", len(stocks))
print("SECTORS:")
for s in sectors:
    print(s, ":", sectors[s])
