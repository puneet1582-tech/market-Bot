# PORTFOLIO RISK BALANCER ENGINE
# Adjusts allocation to avoid excessive sector concentration

def balance_portfolio(allocation_list, sector_map, max_sector_weight=35):
    try:
        sector_weights = {}
        balanced = []

        for item in allocation_list:
            symbol = item["symbol"]
            weight = item["allocation_percent"]

            sector = "UNKNOWN"
            for s, stocks in sector_map.items():
                if symbol in stocks:
                    sector = s
                    break

            sector_weights.setdefault(sector, 0)
            sector_weights[sector] += weight

            if sector_weights[sector] > max_sector_weight:
                weight = max_sector_weight - (sector_weights[sector] - weight)

            balanced.append({
                "symbol": symbol,
                "allocation_percent": round(max(weight, 0), 2),
                "sector": sector
            })

        return balanced

    except Exception as e:
        print("Risk balancing error:", e)
        return allocation_list
