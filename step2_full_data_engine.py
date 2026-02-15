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
        # NSE cookie init
        self.session.get("https://www.nseindia.com", headers=self.headers)

    def fetch_full_dataset(self, symbol):
        base = symbol.replace(".NS","")

        url = f"https://www.nseindia.com/api/quote-equity?symbol={base}"
        r = self.session.get(url, headers=self.headers)
        data = r.json()

        return {
            "symbol": base,
            "timestamp": str(self.timestamp),
            "price": data["priceInfo"]["lastPrice"],
            "volume": data["securityWiseDP"]["quantityTraded"]
        }
