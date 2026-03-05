import json

INPUT_FILE = "data/news/sector_impact.json"
OUTPUT_FILE = "data/news/stock_impact.json"

SECTOR_STOCKS = {
    "IT":["TCS","INFY","HCLTECH","WIPRO"],
    "BANK":["HDFCBANK","ICICIBANK","SBIN"],
    "METALS":["TATASTEEL","JSWSTEEL","HINDALCO"],
    "OIL_GAS":["ONGC","RELIANCE","OIL"],
    "DEFENCE":["HAL","BEL","BDL"]
}

def map_stocks():

    with open(INPUT_FILE) as f:
        data = json.load(f)

    result = []

    for item in data:

        stocks = []

        for sector in item["sectors"]:
            stocks += SECTOR_STOCKS.get(sector,[])

        item["stocks"] = list(set(stocks))
        result.append(item)

    with open(OUTPUT_FILE,"w") as f:
        json.dump(result,f,indent=2)

    print("Stock mapping done")


if __name__ == "__main__":
    map_stocks()
