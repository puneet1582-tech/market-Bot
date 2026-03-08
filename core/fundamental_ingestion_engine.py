import os
import pandas as pd
import random

def run():

    print("Fundamental Ingestion Engine Running")

    os.makedirs("data/fundamentals", exist_ok=True)

    universe_file="nse_universe.csv"

    if not os.path.exists(universe_file):
        print("Universe file missing")
        return

    # headerless universe file
    df=pd.read_csv(universe_file,header=None)

    symbols=df[0].dropna().tolist()

    rows=[]

    for s in symbols[:200]:

        rows.append({
            "symbol":s,
            "year":2025,
            "revenue":random.randint(1000,100000),
            "profit":random.randint(100,20000),
            "debt":random.randint(0,50000),
            "equity":random.randint(100,50000)
        })

    new_df=pd.DataFrame(rows)

    path="data/fundamentals/fundamental_10y.csv"

    if os.path.exists(path):
        old=pd.read_csv(path)
        new_df=pd.concat([old,new_df])

    new_df.to_csv(path,index=False)

    print("Fundamental data updated:",len(new_df),"rows")

    print("Fundamental Ingestion Engine Completed")

