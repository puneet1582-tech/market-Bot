"""
Ultimate Brain — NSE Universe Master Builder
Automatically builds and updates full NSE stock universe list.
"""

import requests
import pandas as pd
from datetime import datetime

NSE_SYMBOL_URL = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
OUTPUT_FILE = "nse_universe_master.csv"


def download_universe():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(NSE_SYMBOL_URL, headers=headers, timeout=30)
    r.raise_for_status()

    df = pd.read_csv(pd.compat.StringIO(r.text))
    df["SYMBOL_NS"] = df["SYMBOL"] + ".NS"

    df.to_csv(OUTPUT_FILE, index=False)

    return {
        "timestamp": str(datetime.utcnow()),
        "symbols_count": len(df)
    }


# DISABLED ENTRY POINT
# if __name__ == "__main__":
    print(download_universe())
