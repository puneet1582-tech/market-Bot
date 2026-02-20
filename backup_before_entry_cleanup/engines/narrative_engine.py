import pandas as pd

NEWS_PATH = "data/internet_news.csv"
STOCKS_PATH = "data/stocks.csv"

class NarrativeEngine:
    def __init__(self):
        self.news = pd.read_csv(NEWS_PATH)
        self.stocks = pd.read_csv(STOCKS_PATH)

    def generate_report(self):
        report = {}

        # Sector sentiment from internet
        sector_sentiment = {}
        for _, row in self.news.iterrows():
            sector = row["sector"]
            sentiment = row["sentiment"]

            if sector not in sector_sentiment:
                sector_sentiment[sector] = {"POSITIVE": 0, "NEGATIVE": 0}

            sector_sentiment[sector][sentiment] += 1

        positive_sectors = []
        negative_sectors = []

        for sector, counts in sector_sentiment.items():
            if counts["POSITIVE"] > counts["NEGATIVE"]:
                positive_sectors.append(sector)
            elif counts["NEGATIVE"] > counts["POSITIVE"]:
                negative_sectors.append(sector)

        # Map sectors to stocks
        likely_gainers = self.stocks[self.stocks["sector"].isin(positive_sectors)]
        likely_losers = self.stocks[self.stocks["sector"].isin(negative_sectors)]

        # Build article style output
        article = {}
        article["summary"] = "Global and internet narrative compared with sector data."

        article["positive_sectors"] = positive_sectors
        article["negative_sectors"] = negative_sectors

        article["likely_gainers"] = likely_gainers["symbol"].tolist()
        article["likely_losers"] = likely_losers["symbol"].tolist()

        article["evidence"] = self.news.to_dict(orient="records")

        article["suggestion"] = {
            "BUY_OR_ACCUMULATE": article["likely_gainers"],
            "SELL_OR_AVOID": article["likely_losers"]
        }

        return article
