import pandas as pd

DATA_PATH = "data/technical.csv"

class TechnicalEngine:
    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)

    def analyze(self, symbol):
        df = self.df[self.df["stock"] == symbol]

        if df.empty:
            return {
                "symbol": symbol,
                "decision": "NO DECISION",
                "reason": "NO TECHNICAL DATA"
            }

        row = df.iloc[0]

        rsi = row["rsi"]
        trend = row["trend"]

        return {
            "symbol": symbol,
            "trend": trend,
            "rsi": rsi
        }
