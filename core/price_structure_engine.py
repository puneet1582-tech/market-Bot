import pandas as pd

class PriceStructureEngine:

    def __init__(self):
        self.price_file = "data/price_history.csv"

    def run(self):

        print("Price Structure Engine Running")

        try:
            df = pd.read_csv(self.price_file)
        except:
            return {}

        if "symbol" not in df.columns:
            return {}

        structure = {}

        for _, row in df.iterrows():

            symbol = row.get("symbol")

            try:
                change = float(row.get("price_change",0))
            except:
                change = 0

            if change > 2:
                structure[symbol] = "STRONG"
            elif change < -2:
                structure[symbol] = "WEAK"
            else:
                structure[symbol] = "NEUTRAL"

        print("Price Structure Engine Completed")

        return structure


def run():

    engine = PriceStructureEngine()

    return engine.run()


if __name__ == "__main__":
    run()
