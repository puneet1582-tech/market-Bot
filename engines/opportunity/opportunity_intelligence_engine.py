import pandas as pd
import os


ALPHA_FILE = "data/processed/alpha_opportunities.csv"
FLOW_FILE = "data/processed/stock_money_flow.csv"
SECTOR_FLOW = "data/processed/sector_money_flow.csv"
SIGNAL_FILE = "data/processed/signal_matrix.csv"
MACRO_FILE = "data/processed/global_sector_impact.csv"

OUTPUT_FILE = "data/processed/opportunity_intelligence.csv"


def safe_read(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def detect_flow_column(df):

    candidates = [
        "money_flow",
        "flow",
        "net_flow",
        "capital_flow"
    ]

    for c in candidates:
        if c in df.columns:
            return c

    return None


def classify_opportunity(row):

    alpha = str(row.get("alpha_adjusted",""))
    flow = row.get("money_flow",0)
    macro = str(row.get("macro_signal",""))

    if alpha == "COMPOUNDING_ALPHA" and flow > 0:
        return "INSTITUTIONAL_COMPOUNDER"

    if alpha == "ROTATION_ALPHA" and flow > 0:
        return "SECTOR_ROTATION"

    if alpha == "MOMENTUM_ALPHA":
        return "MOMENTUM_OPPORTUNITY"

    if macro == "NEGATIVE":
        return "MACRO_RISK"

    return "WATCH"


def run():

    alpha = safe_read(ALPHA_FILE)
    flow = safe_read(FLOW_FILE)
    sector_flow = safe_read(SECTOR_FLOW)
    signals = safe_read(SIGNAL_FILE)
    macro = safe_read(MACRO_FILE)

    if alpha.empty:
        print("Alpha data missing")
        return

    df = alpha.copy()

    if not signals.empty:
        df = df.merge(signals,on="symbol",how="left")

    if not macro.empty:
        df = df.merge(macro,on="sector",how="left")

    if not flow.empty:

        col = detect_flow_column(flow)

        if col:

            flow = flow.rename(columns={col:"money_flow"})

            df = df.merge(
                flow[["symbol","money_flow"]],
                on="symbol",
                how="left"
            )

        else:

            df["money_flow"] = 0

    else:

        df["money_flow"] = 0


    df["opportunity_type"] = df.apply(
        classify_opportunity,
        axis=1
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Opportunity intelligence complete")
    print("Rows:",len(df))


if __name__ == "__main__":
    run()
