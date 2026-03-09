import pandas as pd

class IntelligenceEngine:

    def __init__(self):

        self.price_file = "data/price_history.csv"
        self.fundamental_file = "data/fundamentals.csv"
        self.fii_file = "data/fii_dii.csv"

    def run(self):

        print("Running intelligence layer")

        try:
            price = pd.read_csv(self.price_file)
        except:
            price = pd.DataFrame()

        try:
            fundamentals = pd.read_csv(self.fundamental_file)
        except:
            fundamentals = pd.DataFrame()

        try:
            fii = pd.read_csv(self.fii_file)
        except:
            fii = pd.DataFrame()

        report = {}

        if not price.empty:
            report["stocks_loaded"] = len(price)

        if not fundamentals.empty:
            report["fundamental_records"] = len(fundamentals)

        if not fii.empty:
            report["institutional_records"] = len(fii)

        print("Intelligence Engine completed")

        return report


def run():

    engine = IntelligenceEngine()

    return engine.run()


if __name__ == "__main__":
    run()
