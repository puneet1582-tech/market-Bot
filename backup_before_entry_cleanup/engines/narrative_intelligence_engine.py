"""
Ultimate Brain — Institutional Narrative Intelligence Engine
Maps macro narratives to sectors and opportunity themes.
"""

from datetime import datetime

NARRATIVE_SECTOR_MAP = {
    "AI_BOOM": ["IT", "SEMICONDUCTOR", "DATA_CENTERS"],
    "INFRA_CYCLE": ["INFRA", "CEMENT", "CAPITAL_GOODS"],
    "DEFENSE_CYCLE": ["DEFENSE", "AEROSPACE"],
    "ENERGY_TRANSITION": ["RENEWABLES", "EV", "BATTERY"]
}


def map_narrative(narrative):
    sectors = NARRATIVE_SECTOR_MAP.get(narrative, [])

    return {
        "timestamp": str(datetime.utcnow()),
        "narrative": narrative,
        "impacted_sectors": sectors
    }
