import pandas as pd
import os

INPUT_DIR="data/historical_prices"
OUTPUT="data/processed/market_prices.csv"


def run():

    files=os.listdir(INPUT_DIR)

    all_data=[]

    for f in files:

        if not f.endswith(".csv"):
            continue

        path=os.path.join(INPUT_DIR,f)

        try:

            df=pd.read_csv(path)

            if "symbol" not in df.columns:
                continue

            df=df.rename(columns={
                "Date":"date",
                "Open":"open",
                "High":"high",
                "Low":"low",
                "Close":"close",
                "Volume":"volume"
            })

            df=df[["date","symbol","open","high","low","close","volume"]]

            all_data.append(df)

        except Exception as e:

            print("skip",f,e)


    if len(all_data)==0:

        print("no data found")
        return


    master=pd.concat(all_data)

    master.sort_values(["date","symbol"],inplace=True)

    master.to_csv(OUTPUT,index=False)

    print("MASTER PRICE DATABASE CREATED")


if __name__=="__main__":
    run()
