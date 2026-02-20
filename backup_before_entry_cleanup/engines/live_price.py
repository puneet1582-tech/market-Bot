import yfinance as yf

def live_price(yahoo_symbol):
    try:
        ticker = yf.Ticker(yahoo_symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            return round(data["Close"].iloc[-1], 2)
    except:
        pass
    return "NA"

