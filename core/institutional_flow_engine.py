import pandas as pd

class InstitutionalFlowEngine:

    def __init__(self):

        self.fii_file = "data/fii_dii.csv"
        self.promoter_file = "data/promoter_holdings.csv"

    def run(self):

        print("Institutional Flow Engine Running")

        try:
            fii = pd.read_csv(self.fii_file)
        except:
            fii = pd.DataFrame()

        try:
            promoter = pd.read_csv(self.promoter_file)
        except:
            promoter = pd.DataFrame()

        signals = []

        if not fii.empty:

            for _, row in fii.iterrows():

                try:
                    if row.get("fii_change",0) > 0:

                        signals.append({
                            "symbol": row.get("symbol"),
                            "signal": "FII_ACCUMULATION"
                        })

                except:
                    continue

        if not promoter.empty:

            for _, row in promoter.iterrows():

                try:
                    if row.get("promoter_change",0) > 0:

                        signals.append({
                            "symbol": row.get("symbol"),
                            "signal": "PROMOTER_BUYING"
                        })

                except:
                    continue

        print("Institutional Flow Engine Completed")

        return signals


def run():

    engine = InstitutionalFlowEngine()

    return engine.run()


if __name__ == "__main__":
    run()
