"""
Ultimate Brain — Opportunity Theme Aggregation Engine
Combines narrative, policy, liquidity, and sector-rotation signals
to produce emerging institutional investment themes.
"""

from datetime import datetime


def aggregate_themes(narrative_data, policy_signal, liquidity_signal, sector_rotation):
    themes = []

    # Narrative-driven themes
    for n in narrative_data:
        sectors = n.get("impacted_sectors", [])
        if sectors:
            themes.append({
                "theme_type": "NARRATIVE",
                "source": n.get("narrative"),
                "sectors": sectors
            })

    # Policy-driven themes
    if policy_signal.get("market_impact_signal") == "POSITIVE_EQUITY":
        themes.append({
            "theme_type": "POLICY",
            "source": policy_signal.get("policy_event"),
            "sectors": sector_rotation.get("next_cycle_leaders", [])
        })

    # Liquidity-driven themes
    if liquidity_signal.get("liquidity_signal") == "POSITIVE_LIQUIDITY":
        themes.append({
            "theme_type": "LIQUIDITY",
            "source": "FII_DII_FLOW",
            "sectors": sector_rotation.get("next_cycle_leaders", [])
        })

    return {
        "timestamp": str(datetime.utcnow()),
        "emerging_themes": themes
    }
