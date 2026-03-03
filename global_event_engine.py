import csv

class GlobalEventEngine:

    def __init__(self):
        self.current_event = "WAR"

        self.event_sector_impact = {
            "WAR": {
                "DEFENSE": 15,
                "OIL": 10,
                "AVIATION": -12,
                "BANKING": 0
            }
        }

    def get_sector_impact(self, sector):
        return self.event_sector_impact.get(self.current_event, {}).get(sector.upper(), 0)
