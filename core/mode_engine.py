import pandas as pd

class MarketModeEngine:

    def __init__(self):
        self.index_file = "data/nifty_index.csv"
        self.volatility_file = "data/nifty_volatility.csv"

    def run(self):

        print("Market Mode Engine Running")

        try:
            index = pd.read_csv(self.index_file)
        except:
            index = pd.DataFrame()

        try:
            vol = pd.read_csv(self.volatility_file)
        except:
            vol = pd.DataFrame()

        mode = "UNKNOWN"

        try:

            if not index.empty and "change_pct" in index.columns:

                change = float(index.iloc[-1]["change_pct"])

                if change > 1:
                    mode = "INVEST"

                elif change < -1:
                    mode = "DEFENSIVE"

                else:
                    mode = "TRADE"

        except:
            pass

        result = {
            "market_mode": mode
        }

        print("Market Mode Engine Completed")

        return result


def run():

    engine = MarketModeEngine()

    return engine.run()


if __name__ == "__main__":
    run()
