import yfinance as yf

def get_live_price(stock):
    try:
        symbol = stock + ".NS"   # NSE stocks
        data = yf.Ticker(symbol)
        price = data.info.get("regularMarketPrice", None)
        return price
    except:
        return None
