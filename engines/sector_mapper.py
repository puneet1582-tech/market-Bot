def map_by_sector(stocks):
    sector_map = {}

    for stock in stocks:
        sector = stock["sector"]
        symbol = stock["symbol"]

        if sector not in sector_map:
            sector_map[sector] = []

        sector_map[sector].append(symbol)

    return sector_map

