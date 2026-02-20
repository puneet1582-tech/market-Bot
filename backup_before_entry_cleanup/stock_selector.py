from fundamental_brain import fundamental_data

def select_stocks(mode):
    invest_stocks = []
    trade_stocks = []
    defensive_stocks = []

    for stock, data in fundamental_data.items():
        if data["risk"] == "LOW":
            invest_stocks.append(stock)
            defensive_stocks.append(stock)
        elif data["risk"] == "MEDIUM":
            trade_stocks.append(stock)
        else:
            pass

    if mode == "INVEST MODE":
        return invest_stocks
    elif mode == "TRADE MODE":
        return trade_stocks
    elif mode == "DEFENSIVE MODE":
        return defensive_stocks
    else:
        return []

# TEST
mode = "DEFENSIVE MODE"
selected = select_stocks(mode)

print("MODE:", mode)
print("SELECTED STOCKS:", selected)
