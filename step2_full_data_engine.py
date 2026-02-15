import requests
from datetime import datetime

class FullDataEngine:

    def __init__(self):
        self.timestamp = datetime.now()
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.session.get("https://www.nseindia.com", headers=self.headers)

    def fetch_full_dataset(self, symbol):
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol.replace('.NS','')}"
        r = self.session.get(url, headers=self.headers)
        data = r.json()

        price = data["priceInfo"]["lastPrice"]
        volume = data["securityWiseDP"]["quantityTraded"]

        return {
            "symbol": symbol,
            "price": price,
            "volume": volume,
            "timestamp": str(self.timestamp)
        }

