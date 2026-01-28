import pandas as pd

DATA_PATH = "data/nifty_index.csv"

class IndexEngine:
    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)

    def get_trend(self):
        if len(self.df) < 10:
            return "UNKNOWN"

        self.df["Close"] = pd.to_numeric(self.df["Close"], errors="coerce")

        last_5 = self.df["Close"].tail(5)
        first = last_5.iloc[0]
        last = last_5.iloc[-1]

        pct = (last - first) / first * 100

        if pct > 1:
            return "UP"
        elif pct < -1:
            return "DOWN"
        else:
            return "SIDEWAYS"
