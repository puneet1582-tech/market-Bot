import json

INPUT_FILE = "data/news/global_news.json"
OUTPUT_FILE = "data/news/validated_news.json"

TRUSTED = ["reuters", "bbc", "cnbc"]

def validate_news():

    with open(INPUT_FILE) as f:
        data = json.load(f)

    validated = []

    for item in data:
        for source in TRUSTED:
            if source in item["source"].lower():
                validated.append(item)
                break

    with open(OUTPUT_FILE, "w") as f:
        json.dump(validated, f, indent=2)

    print("Validated news:", len(validated))


if __name__ == "__main__":
    validate_news()
