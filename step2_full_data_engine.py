import yfinance as yf
from datetime import datetime

class FullDataEngine:
    def __init__(self):
        self.timestamp = datetime.now()

    def fetch_full_dataset(self, symbol):
        ticker = yf.Ticker(symbol)
        return {
            'symbol': symbol,
            'timestamp': str(self.timestamp),
            'price_data': ticker.history(period='1y')
        }
