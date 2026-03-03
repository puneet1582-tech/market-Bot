class GlobalEventEngine:

    def __init__(self):
        self.current_event = "WAR"

        self.event_sector_impact = {
            "WAR": {
                "DEFENSE": 15,
                "ENERGY": 12,
                "OIL": 12,
                "METALS": 8,
                "IT": -5,
                "BANK": -3,
                "BANKING": -3,
                "AVIATION": -15,
                "REALTY": -7,
                "AUTO": -6,
                "SMALL_CAP": -4
            }
        }

    def get_sector_impact(self, sector):
        return self.event_sector_impact.get(self.current_event, {}).get(sector.upper(), 0)
