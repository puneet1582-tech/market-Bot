"""
INSTITUTIONAL GRADE LIVE PRICE INGESTION ENGINE
Multi-source resilient live NSE price fetch
"""

from datetime import datetime
import time

def _fetch_from_yfinance(symbol):
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")
        if not data.empty:
            latest = data.iloc[-1]
            return float(latest["Close"]), int(latest["Volume"])
    except Exception:
        pass
    return None, None


def _fetch_from_nse(symbol):
    try:
        from nsepython import nse_eq
        q = nse_eq(symbol.replace(".NS", ""))
        return float(q["priceInfo"]["lastPrice"]), int(q["securityWiseDP"]["deliveryQuantity"])
    except Exception:
        pass
    return None, None


def fetch_price(symbol):
    for _ in range(2):
        price, volume = _fetch_from_yfinance(symbol)
        if price:
            return {
                "symbol": symbol,
                "price": price,
                "volume": volume or 0,
                "timestamp": str(datetime.utcnow())
            }

        price, volume = _fetch_from_nse(symbol)
        if price:
            return {
                "symbol": symbol,
                "price": price,
                "volume": volume or 0,
                "timestamp": str(datetime.utcnow())
            }

        time.sleep(1)

    return {
        "symbol": symbol,
        "price": 0,
        "volume": 0,
        "timestamp": str(datetime.utcnow())
    }
