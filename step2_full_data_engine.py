# SAFE FALLBACK DATA ENGINE (NO NSEPYTHON DEPENDENCY)

import requests

def fetch_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        r = requests.get(url, timeout=10)
        data = r.json()
        return data["quoteResponse"]["result"][0]["regularMarketPrice"]
    except:
        return 0
