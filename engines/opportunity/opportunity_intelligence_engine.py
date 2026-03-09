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


def classify_opportunity(row):

    alpha = str(row.get("alpha_adjusted",""))
    flow = row.get("money_flow",0)
    sector_flow = row.get("sector_flow",0)
    macro = str(row.get("macro_signal",""))

    if alpha == "COMPOUNDING_ALPHA" and flow > 0 and sector_flow > 0:
        return "INSTITUTIONAL_COMPOUNDER"

    if alpha == "ROTATION_ALPHA" and sector_flow > 0:
        return "SECTOR_ROTATION_PLAY"

    if alpha == "MOMENTUM_ALPHA" and flow > 0:
        return "MOMENTUM_BREAKOUT"

    if macro == "NEGATIVE":
        return "MACRO_RISK"

    return "WATCHLIST"


def run():

    alpha = safe_read(ALPHA_FILE)
    flow = safe_read(FLOW_FILE)
    sector = safe_read(SECTOR_FLOW)
    signals = safe_read(SIGNAL_FILE)
    macro = safe_read(MACRO_FILE)

    if signals.empty:
        print("Signal data missing")
        return

    df = signals.copy()

    if not alpha.empty:
        df = df.merge(alpha[["symbol","alpha_adjusted"]],on="symbol",how="left")

    if not flow.empty:
        df = df.merge(flow[["symbol","money_flow"]],on="symbol",how="left")

    if not sector.empty:
        df = df.merge(sector[["sector","sector_flow"]],on="sector",how="left")

    if not macro.empty:
        df = df.merge(macro,on="sector",how="left")

    df["opportunity_type"] = df.apply(classify_opportunity,axis=1)

    df.to_csv(OUTPUT_FILE,index=False)

    print("Opportunity intelligence generated")
    print("Rows:",len(df))


if __name__ == "__main__":
    run()
