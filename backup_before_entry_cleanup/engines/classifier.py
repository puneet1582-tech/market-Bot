# -------- NEW ATH + SECTOR LOGIC --------

def stock_universe():
    return {
        "IT": ["TCS", "INFY"],
        "BANK": ["HDFCBANK", "ICICIBANK"],
        "ENERGY": ["RELIANCE"]
    }

def ath_data():
    return {
        "TCS": {"ath": 4100, "current": 3800},
        "INFY": {"ath": 1900, "current": 1600},
        "RELIANCE": {"ath": 3100, "current": 3100}
    }

def ath_bucket(stock):
    data_dict = ath_data()

    if stock not in data_dict:
        return "NO ATH DATA"

    data = data_dict[stock]
    drop = (data["ath"] - data["current"]) / data["ath"] * 100

    if drop >= 70:
        return "70% DOWN"
    elif drop >= 50:
        return "50% DOWN"
    elif drop >= 30:
        return "30% DOWN"
    else:
        return "LESS THAN 30%"

