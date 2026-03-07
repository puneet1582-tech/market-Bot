import os
import pandas as pd

FUNDAMENTAL_PATH = "data/fundamentals"


class BuffettBusinessQualityEngine:

    def load_fundamentals(self):

        if not os.path.exists(FUNDAMENTAL_PATH):
            print("Fundamental database missing")
            return None

        files = os.listdir(FUNDAMENTAL_PATH)

        data = []

        for f in files:

            try:
                df = pd.read_csv(os.path.join(FUNDAMENTAL_PATH, f))
                data.append(df)
            except:
                continue

        if not data:
            return None

        return pd.concat(data)


    def analyze_company(self, df):

        try:

            revenue_growth = df["revenue"].pct_change().mean()

            profit_growth = df["net_profit"].pct_change().mean()

            roe = df["roe"].mean()

            debt_ratio = df["debt"] / df["revenue"]

            avg_debt = debt_ratio.mean()

            score = 0

            if revenue_growth > 0.10:
                score += 1

            if profit_growth > 0.10:
                score += 1

            if roe > 15:
                score += 1

            if avg_debt < 0.5:
                score += 1

            if score == 4:
                return "COMPOUNDER"

            if score == 3:
                return "STRONG"

            if score == 2:
                return "AVERAGE"

            return "WEAK"

        except:
            return "UNKNOWN"


    def run(self):

        print("\nBUFFETT BUSINESS QUALITY ANALYSIS\n")

        df = self.load_fundamentals()

        if df is None:
            print("Fundamental data not available")
            return

        results = []

        for symbol in df["symbol"].unique():

            company = df[df["symbol"] == symbol]

            quality = self.analyze_company(company)

            results.append({
                "symbol": symbol,
                "quality": quality
            })

        result_df = pd.DataFrame(results)

        os.makedirs("data/intelligence", exist_ok=True)

        result_df.to_csv("data/intelligence/buffett_quality.csv", index=False)

        print("Buffett analysis complete")


if __name__ == "__main__":
    pass

    engine = BuffettBusinessQualityEngine()

    engine.run()
