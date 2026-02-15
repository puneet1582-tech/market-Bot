import requests
from datetime import datetime

class FullDataEngine:

    def __init__(self):
        self.timestamp = datetime.now()
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br"
        }

        # NSE cookie initialization
        self.session.get("https://www.nseindia.com", headers=self.headers)

    def fetch_full_dataset(self, symbol):

        symbol_clean = symbol.replace(".NS", "")

        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol_clean}"

        r = self.session.get(url, headers=self.headers)

        if r.status_code != 200:
            return {
                "symbol": symbol,
                "price": 0,
                "volume": 0,
                "timestamp": str(self.timestamp)
            }

        data = r.json()

        return {
            "symbol": symbol,
            "price": data["priceInfo"]["lastPrice"],
            "volume": data["securityWiseDP"]["quantityTraded"],
            "timestamp": str(self.timestamp)
        }
