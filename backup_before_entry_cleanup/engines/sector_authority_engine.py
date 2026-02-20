"""
SECTOR AUTHORITY ENGINE
Institutional Multi-Layer Sector Classification Controller
Priority:
1. NSE Official Index Layer
2. Keyword Intelligence Layer
"""

import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

INDEX_FILE = "data/sector_index_base.csv"
KEYWORD_FILE = "data/sector_master.csv"
OUTPUT_FILE = "data/sector_final_authority.csv"


def load_layers():
    index_df = pd.read_csv(INDEX_FILE)
    keyword_df = pd.read_csv(KEYWORD_FILE)
    return index_df, keyword_df


def build_authority(index_df, keyword_df):

    index_df = index_df[["symbol", "sector"]].copy()
    keyword_df = keyword_df[["symbol", "sector"]].copy()

    index_df["priority"] = 1
    keyword_df["priority"] = 2

    combined = pd.concat([index_df, keyword_df], ignore_index=True)

    combined.sort_values(by="priority", inplace=True)
    combined.drop_duplicates(subset=["symbol"], keep="first", inplace=True)

    combined["computed_time"] = datetime.utcnow()

    return combined[["symbol", "sector", "computed_time"]]


def run_sector_authority_engine():
    logging.info("SECTOR AUTHORITY ENGINE STARTED")

    index_df, keyword_df = load_layers()

    final_df = build_authority(index_df, keyword_df)

    final_df.to_csv(OUTPUT_FILE, index=False)

    logging.info(f"FINAL SECTOR AUTHORITY BUILT. Total symbols: {len(final_df)}")


# DISABLED ENTRY POINT
# if __name__ == "__main__":
    run_sector_authority_engine()
