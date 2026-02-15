from step2_full_data_engine import FullDataEngine

class BrainEngine:
    def __init__(self):
        self.data_engine = FullDataEngine()

    def analyze_stock(self, symbol):
        data = self.data_engine.fetch_full_dataset(symbol)
        return {
            "symbol": data["symbol"],
            "records_price": len(data["price_data"]),
            "timestamp": data["timestamp"]
        }
