def why_engine(market_mode, market_why, sector_result, stock_result, money_flow_result, risk):
    reasons = []

    # Market WHY
    reasons.append(f"Market: {market_mode} ({market_why})")

    # Money Flow WHY
    if money_flow_result:
        reasons.append(f"Money flow: {money_flow_result.get('reason')}")

    # Sector WHY
    if sector_result:
        sector, score, sector_why = sector_result
        reasons.append(f"Sector: {sector} (score {score}) because {sector_why}")

    # Stock WHY
    if stock_result:
        reasons.append(f"Stock: {stock_result['symbol']} because {stock_result['why']}")

    # Risk
    reasons.append(f"Risk level: {risk}")

    return " | ".join(reasons)
