import json

INPUT_FILE = "data/news/macro_events.json"
OUTPUT_FILE = "data/news/sector_impact.json"

MAP = {
    "INTEREST_RATE": ["BANK","NBFC","REAL_ESTATE"],
    "OIL": ["OIL_GAS","PAINT","AIRLINES"],
    "TECH_POLICY": ["IT","SEMICONDUCTOR"],
    "GEOPOLITICS": ["DEFENCE","METALS"]
}

def map_sector():

    with open(INPUT_FILE) as f:
        events = json.load(f)

    impacts = []

    for e in events:

        sectors = MAP.get(e["macro_event"],["GENERAL"])

        e["sectors"] = sectors
        impacts.append(e)

    with open(OUTPUT_FILE,"w") as f:
        json.dump(impacts,f,indent=2)

    print("Sector mapping complete")


if __name__ == "__main__":
    map_sector()
