import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def fetch_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        r = requests.get(url, headers=HEADERS, timeout=10)

        if r.status_code != 200:
            print("YAHOO HTTP ERROR:", r.status_code)
            return None

        data = r.json()
        result = data.get("quoteResponse", {}).get("result", [])

        if not result:
            print("YAHOO EMPTY RESULT")
            return None

        price = result[0].get("regularMarketPrice")

        if price is None:
            print("YAHOO PRICE NONE")
            return None

        return price

    except Exception as e:
        print("YAHOO FETCH ERROR:", e)
        return None


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
