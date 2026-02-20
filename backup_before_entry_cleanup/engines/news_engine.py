import pandas as pd

DATA_PATH = "data/news.csv"

class NewsEngine:
    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)

    def analyze(self, sector):
        df = self.df[self.df["sector"] == sector]

        if df.empty:
            return {
                "sector": sector,
                "news_impact": "NEUTRAL",
                "reason": "NO NEWS"
            }

        positives = df[df["impact"] == "POSITIVE"]
        negatives = df[df["impact"] == "NEGATIVE"]

        if len(positives) > len(negatives):
            impact = "POSITIVE"
        elif len(negatives) > len(positives):
            impact = "NEGATIVE"
        else:
            impact = "NEUTRAL"

        return {
            "sector": sector,
            "news_impact": impact,
            "headlines": df["headline"].tolist()
        }
