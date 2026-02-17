"""
ULTIMATE BRAIN — INSTITUTIONAL MARKET DATA INGESTION ENGINE
High reliability multi-provider live price ingestion
"""

import time
import logging
from datetime import datetime
from cachetools import TTLCache

log = logging.getLogger("ingestion")
cache = TTLCache(maxsize=5000, ttl=20)


def _safe_yfinance(symbol):
    try:
        import yfinance as yf
        d = yf.Ticker(symbol).history(period="1d", interval="1m")
        if not d.empty:
            r = d.iloc[-1]
            return float(r["Close"]), int(r["Volume"])
    except Exception as e:
        log.debug(f"yfinance fail {symbol}: {e}")
    return None, None


def _safe_nse(symbol):
    try:
        from nsepython import nse_eq
        q = nse_eq(symbol.replace(".NS", ""))
        return float(q["priceInfo"]["lastPrice"]), int(q["securityWiseDP"]["deliveryQuantity"])
    except Exception as e:
        log.debug(f"nse fail {symbol}: {e}")
    return None, None


def fetch_price(symbol):
    if symbol in cache:
        return cache[symbol]

    providers = (_safe_yfinance, _safe_nse)

    for attempt in range(3):
        for provider in providers:
            price, vol = provider(symbol)
            if price:
                data = {
                    "symbol": symbol,
                    "price": price,
                    "volume": vol or 0,
                    "timestamp": str(datetime.utcnow())
                }
                cache[symbol] = data
                return data
        time.sleep(1.5 * (attempt + 1))

    fallback = {
        "symbol": symbol,
        "price": 0,
        "volume": 0,
        "timestamp": str(datetime.utcnow())
    }
    cache[symbol] = fallback
    return fallback
