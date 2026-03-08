import os
import pandas as pd

def run():

    print("10 Year Fundamental Engine Running")

    os.makedirs("data/fundamentals", exist_ok=True)

    path="data/fundamentals/fundamental_10y.csv"

    if not os.path.exists(path):

        df=pd.DataFrame(columns=[
            "symbol",
            "year",
            "revenue",
            "profit",
            "debt",
            "equity"
        ])

        df.to_csv(path,index=False)

        print("10Y fundamental database initialized")

    else:

        df=pd.read_csv(path)

        print("10Y fundamental database loaded:",len(df),"rows")

    print("10 Year Fundamental Engine Completed")

