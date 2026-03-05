import json

INPUT_FILE = "data/news/validated_news.json"
OUTPUT_FILE = "data/news/macro_events.json"

KEYWORDS = {
    "INTEREST_RATE": ["rate hike","interest rate","fed","central bank"],
    "OIL": ["oil","opec","crude"],
    "TECH_POLICY": ["chip","ai","semiconductor"],
    "GEOPOLITICS": ["war","sanction","military"],
}

def classify():

    with open(INPUT_FILE) as f:
        news = json.load(f)

    events = []

    for item in news:
        text = item["headline"].lower()

        event_type = "OTHER"

        for k,v in KEYWORDS.items():
            for word in v:
                if word in text:
                    event_type = k

        item["macro_event"] = event_type
        events.append(item)

    with open(OUTPUT_FILE,"w") as f:
        json.dump(events,f,indent=2)

    print("Macro events classified")


if __name__ == "__main__":
    classify()
