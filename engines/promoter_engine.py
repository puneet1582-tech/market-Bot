import pandas as pd

DATA_PATH = "data/fii_dii.csv"

class PromoterEngine:
    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)

    def analyze(self, sector):
        df = self.df[self.df["sector"] == sector]

        if df.empty:
            return {
                "sector": sector,
                "decision": "NO DECISION",
                "reason": "NO FII/DII DATA"
            }

        row = df.iloc[0]

        fii = row["fii"]
        dii = row["dii"]

        fii_signal = "BUYING" if fii > 0 else "SELLING"
        dii_signal = "BUYING" if dii > 0 else "SELLING"

        return {
            "sector": sector,
            "fii": fii_signal,
            "dii": dii_signal
        }
