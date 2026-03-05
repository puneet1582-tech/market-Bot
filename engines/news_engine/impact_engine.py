import json

INPUT_FILE = "data/news/stock_impact.json"

def generate_report():

    with open(INPUT_FILE) as f:
        data = json.load(f)

    print("GLOBAL NEWS IMPACT REPORT")
    print("-"*40)

    for item in data[:10]:

        print("NEWS:", item["headline"])
        print("MACRO:", item["macro_event"])
        print("SECTORS:", item["sectors"])
        print("STOCKS:", item["stocks"])
        print()

if __name__ == "__main__":
    generate_report()
