import pandas as pd
import os


SECTOR_FILE = "data/processed/sector_intelligence.csv"
COMPANY_FILE = "data/processed/company_intelligence.csv"
OWNERSHIP_FILE = "data/processed/ownership_intelligence.csv"
GLOBAL_FILE = "data/processed/global_sector_impact.csv"
MOMENTUM_FILE = "data/processed/momentum_stocks.csv"
UNIVERSE_FILE = "data/processed/tradable_universe.csv"
MAP_FILE = "data/processed/stock_sector_map.csv"

OUTPUT_FILE = "data/processed/signal_matrix.csv"


def safe_read(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def run():

    sector = safe_read(SECTOR_FILE)
    company = safe_read(COMPANY_FILE)
    ownership = safe_read(OWNERSHIP_FILE)
    macro = safe_read(GLOBAL_FILE)
    momentum = safe_read(MOMENTUM_FILE)
    universe = safe_read(UNIVERSE_FILE)
    sector_map = safe_read(MAP_FILE)

    if universe.empty:
        print("Universe empty")
        return

    df = universe.copy()

    if not sector_map.empty:
        df = df.merge(sector_map, on="symbol", how="left")

    if not sector.empty:
        df = df.merge(sector, on="sector", how="left")

    if not company.empty:
        df = df.merge(company, on="symbol", how="left")

    if not ownership.empty:
        df = df.merge(ownership, on="symbol", how="left")

    if not macro.empty:
        df = df.merge(macro, on="sector", how="left")

    if not momentum.empty:
        df["momentum_flag"] = df["symbol"].isin(momentum["symbol"])
    else:
        df["momentum_flag"] = False


    def synthesize(row):

        signals = []

        if str(row.get("business_quality","")) == "WORLD_CLASS":
            signals.append("STRONG_BUSINESS")

        if str(row.get("sector_strength","")) == "STRONG":
            signals.append("STRONG_SECTOR")

        if str(row.get("institutional_activity","")) == "ACCUMULATION":
            signals.append("INSTITUTIONAL_BUYING")

        if row.get("momentum_flag",False):
            signals.append("PRICE_MOMENTUM")

        if str(row.get("macro_signal","")) == "POSITIVE":
            signals.append("GLOBAL_TAILWIND")

        if str(row.get("macro_signal","")) == "NEGATIVE":
            signals.append("GLOBAL_HEADWIND")

        return "|".join(signals)


    df["signals"] = df.apply(synthesize,axis=1)

    df.to_csv(OUTPUT_FILE,index=False)

    print("Signal fusion complete")
    print("Rows:",len(df))


if __name__ == "__main__":
    run()
