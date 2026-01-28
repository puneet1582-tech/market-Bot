fundamental_data = {
    "RELIANCE": {
        "sector": "ENERGY",
        "debt": 150000,
        "sales": 900000,
        "profit": 70000,
        "promoter_holding": 50,
        "fii_holding": 23,
        "risk": "MEDIUM"
    },
    "TCS": {
        "sector": "IT",
        "debt": 0,
        "sales": 250000,
        "profit": 42000,
        "promoter_holding": 72,
        "fii_holding": 18,
        "risk": "LOW"
    },
    "HDFCBANK": {
        "sector": "BANKING",
        "debt": 0,
        "sales": 200000,
        "profit": 60000,
        "promoter_holding": 25,
        "fii_holding": 35,
        "risk": "LOW"
    },
    "ITC": {
        "sector": "FMCG",
        "debt": 0,
        "sales": 70000,
        "profit": 18000,
        "promoter_holding": 0,
        "fii_holding": 12,
        "risk": "LOW"
    }
}

print("FUNDAMENTAL DATA READY")
for stock in fundamental_data:
    print(stock, fundamental_data[stock])
