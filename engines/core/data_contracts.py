import pandas as pd
import os


SCHEMAS = {

"stock_money_flow.csv":[
"symbol",
"money_flow"
],

"sector_money_flow.csv":[
"sector",
"sector_flow"
],

"alpha_opportunities.csv":[
"symbol",
"alpha_adjusted"
],

"signal_matrix.csv":[
"symbol",
"signals"
],

"global_sector_impact.csv":[
"sector",
"macro_signal"
]

}


DATA_DIR = "data/processed"


def ensure_schema(file,columns):

    path = os.path.join(DATA_DIR,file)

    if not os.path.exists(path):

        df = pd.DataFrame(columns=columns)
        df.to_csv(path,index=False)
        return

    df = pd.read_csv(path)

    for c in columns:

        if c not in df.columns:
            df[c] = None

    df = df[columns]

    df.to_csv(path,index=False)



def run():

    for file,cols in SCHEMAS.items():
        ensure_schema(file,cols)

    print("DATA CONTRACT VALIDATION COMPLETE")


if __name__ == "__main__":
    run()
