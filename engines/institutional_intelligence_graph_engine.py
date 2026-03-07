import sys
import os
import pandas as pd

sys.path.append(os.getcwd())


class InstitutionalIntelligenceGraphEngine:

    def load_prices(self):

        path = "data/prices"

        if not os.path.exists(path):
            print("Price data missing")
            return None

        files = os.listdir(path)

        if not files:
            print("No price files found")
            return None

        df_list = []

        for f in files:
            try:
                df = pd.read_csv(os.path.join(path, f))
                df_list.append(df)
            except:
                continue

        if not df_list:
            return None

        return pd.concat(df_list)


    def load_fundamentals(self):

        path = "data/fundamentals"

        if not os.path.exists(path):
            print("Fundamental data missing")
            return None

        files = os.listdir(path)

        df_list = []

        for f in files:
            try:
                df = pd.read_csv(os.path.join(path, f))
                df_list.append(df)
            except:
                continue

        if not df_list:
            return None

        return pd.concat(df_list)


    def load_ownership(self):

        path = "data/ownership"

        if not os.path.exists(path):
            print("Ownership data missing")
            return None

        files = os.listdir(path)

        df_list = []

        for f in files:
            try:
                df = pd.read_csv(os.path.join(path, f))
                df_list.append(df)
            except:
                continue

        if not df_list:
            return None

        return pd.concat(df_list)


    def build_intelligence(self):

        print("\nBuilding Institutional Intelligence Graph\n")

        prices = self.load_prices()
        fundamentals = self.load_fundamentals()
        ownership = self.load_ownership()

        if prices is None:
            print("Price intelligence unavailable")
            return

        if fundamentals is None:
            print("Fundamental intelligence unavailable")
            return

        if ownership is None:
            print("Ownership intelligence unavailable")
            return

        print("Prices loaded:", len(prices))
        print("Fundamentals loaded:", len(fundamentals))
        print("Ownership records:", len(ownership))

        print("\nInstitutional Intelligence Graph Ready\n")


if __name__ == "__main__":

    engine = InstitutionalIntelligenceGraphEngine()

    engine.build_intelligence()
