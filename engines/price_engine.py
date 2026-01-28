import pandas as pd

DATA_PATH = "data/price_data.csv"

class PriceEngine:
    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)

    def analyze(self, symbol):
        df = self.df[self.df["symbol"] == symbol]

        if df.empty or len(df) < 2:
            return {
                "symbol": symbol,
                "decision": "NO DECISION",
                "reason": "NOT ENOUGH PRICE DATA"
            }

        prices = df["price"].astype(float).values

        changes = []
        for i in range(1, len(prices)):
            old = prices[i-1]
            new = prices[i]
            pct = round((new - old) / old * 100, 2)
            changes.append(float(pct))

        ath = float(max(prices))
        current = float(prices[-1])
        ath_drop = round((ath - current) / ath * 100, 2)

        return {
            "symbol": symbol,
            "quarter_changes_percent": changes,
            "ath": ath,
            "current_price": current,
            "ath_drop_percent": float(ath_drop)
        }
