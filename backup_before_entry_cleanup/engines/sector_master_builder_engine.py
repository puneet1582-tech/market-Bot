"""
INSTITUTIONAL SECTOR MASTER BUILDER
Builds Symbol → Sector mapping table (Persistent Master File)
"""

import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

UNIVERSE_FILE = "data/nse_live_universe.csv"
OUTPUT_FILE = "data/sector_master.csv"


def load_universe():
    df = pd.read_csv(UNIVERSE_FILE)
    return df


def build_sector_master(universe_df):
    """
    Institutional-level sector build logic.
    For now: structured classification using company name pattern + fallback.
    Later: NSE official sector ingestion integration.
    """

    sector_rules = {
        "BANK": "Finance",
        "FINANCE": "Finance",
        "NBFC": "Finance",
        "INSURANCE": "Finance",
        "TECH": "IT",
        "SOFTWARE": "IT",
        "INFOTECH": "IT",
        "PHARMA": "Pharma",
        "BIO": "Pharma",
        "AUTO": "Automobile",
        "CEMENT": "Cement",
        "POWER": "Energy",
        "ENERGY": "Energy",
        "STEEL": "Metals",
        "METAL": "Metals",
        "OIL": "Energy",
        "GAS": "Energy"
    }

    records = []

    for _, row in universe_df.iterrows():
        name = str(row["company_name"]).upper()
        symbol = row["symbol"]

        assigned_sector = "Unknown"

        for keyword, sector in sector_rules.items():
            if keyword in name:
                assigned_sector = sector
                break

        records.append({
            "symbol": symbol,
            "sector": assigned_sector,
            "computed_time": datetime.utcnow()
        })

    return pd.DataFrame(records)


def run_sector_master_builder():

    logging.info("SECTOR MASTER BUILD STARTED")

    universe = load_universe()
    sector_master = build_sector_master(universe)

    sector_master.to_csv(OUTPUT_FILE, index=False)

    logging.info(f"SECTOR MASTER BUILT: {len(sector_master)} symbols")


# DISABLED ENTRY POINT
# if __name__ == "__main__":
    run_sector_master_builder()
