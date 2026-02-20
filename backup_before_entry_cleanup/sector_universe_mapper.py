# SECTOR UNIVERSE MAPPER
# Maps stock universe into sector buckets

SECTOR_UNIVERSE = {
    "ENERGY": ["RELIANCE.NS"],
    "IT": ["TCS.NS", "INFY.NS"],
    "BANKING": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS"],
    "FMCG": ["HINDUNILVR.NS", "ITC.NS"],
    "INFRA": ["LT.NS"],
    "TELECOM": ["BHARTIARTL.NS"]
}

def map_sector_universe(stocks):
    sector_map = {}

    for sector, sector_stocks in SECTOR_UNIVERSE.items():
        sector_map[sector] = [s for s in stocks if s in sector_stocks]

    return sector_map
