import pandas as pd
import os


SIGNAL_FILE = "data/processed/signal_matrix.csv"
MARKET_FILE = "data/processed/market_mode.csv"

OUTPUT_FILE = "data/processed/alpha_opportunities.csv"


def safe_read(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def classify_alpha(signal_string):

    s = str(signal_string)

    strong_business = "STRONG_BUSINESS" in s
    strong_sector = "STRONG_SECTOR" in s
    inst_buying = "INSTITUTIONAL_BUYING" in s
    momentum = "PRICE_MOMENTUM" in s
    macro_tailwind = "GLOBAL_TAILWIND" in s
    macro_headwind = "GLOBAL_HEADWIND" in s

    if strong_business and strong_sector and inst_buying and macro_tailwind:
        return "COMPOUNDING_ALPHA"

    if strong_sector and momentum and inst_buying:
        return "ROTATION_ALPHA"

    if strong_business and momentum:
        return "MOMENTUM_ALPHA"

    if macro_headwind:
        return "MACRO_RISK"

    return "NEUTRAL"


def run():

    signals = safe_read(SIGNAL_FILE)
    market = safe_read(MARKET_FILE)

    if signals.empty:
        print("Signal matrix missing")
        return

    df = signals.copy()

    df["alpha_type"] = df["signals"].apply(classify_alpha)

    market_mode = "NEUTRAL"
    if not market.empty:
        market_mode = market.iloc[0]["market_mode"]

    def adjust_for_market(row):

        alpha = row["alpha_type"]

        if market_mode == "RISK" and alpha in ["ROTATION_ALPHA","MOMENTUM_ALPHA"]:
            return "WEAK_ALPHA"

        return alpha

    df["alpha_adjusted"] = df.apply(adjust_for_market,axis=1)

    alpha_df = df[df["alpha_adjusted"].isin([
        "COMPOUNDING_ALPHA",
        "ROTATION_ALPHA",
        "MOMENTUM_ALPHA"
    ])]

    alpha_df = alpha_df.sort_values(by="alpha_adjusted")

    alpha_df.to_csv(OUTPUT_FILE,index=False)

    print("Alpha discovery complete")
    print("Opportunities:",len(alpha_df))


if __name__ == "__main__":
    run()
