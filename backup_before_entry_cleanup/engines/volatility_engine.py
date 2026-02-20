import pandas as pd

DATA_PATH = "data/nifty_volatility.csv"

class VolatilityEngine:
    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)

    def get_volatility_state(self):
        if len(self.df) < 10:
            return "UNKNOWN"

        self.df["volatility"] = pd.to_numeric(self.df["volatility"], errors="coerce")

        recent = self.df["volatility"].tail(5).mean()

        if recent > 0.02:
            return "HIGH"
        else:
            return "LOW"
