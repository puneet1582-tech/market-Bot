import pandas as pd
import os


FLOW_FILE = "data/processed/stock_money_flow.csv"
SECTOR_FILE = "data/processed/sector_money_flow.csv"


FLOW_CANDIDATES = [
"money_flow",
"flow",
"net_flow",
"capital_flow"
]


def normalize_stock_flow():

    if not os.path.exists(FLOW_FILE):
        return

    df = pd.read_csv(FLOW_FILE)

    flow_col = None

    for c in FLOW_CANDIDATES:
        if c in df.columns:
            flow_col = c
            break

    if flow_col and flow_col != "money_flow":
        df = df.rename(columns={flow_col:"money_flow"})

    df.to_csv(FLOW_FILE,index=False)


def normalize_sector_flow():

    if not os.path.exists(SECTOR_FILE):
        return

    df = pd.read_csv(SECTOR_FILE)

    if "flow" in df.columns and "sector_flow" not in df.columns:
        df = df.rename(columns={"flow":"sector_flow"})

    df.to_csv(SECTOR_FILE,index=False)


def run():

    normalize_stock_flow()
    normalize_sector_flow()

    print("SCHEMA NORMALIZATION COMPLETE")


if __name__ == "__main__":
    run()
