import csv

def load_shark_data(filepath="data/shark.csv"):
    data = {}
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row["stock"]] = row["volume_spike"]
    return data

def shark_signal(stock, shark_data):
    if stock not in shark_data:
        return "NO DATA"
    if shark_data[stock] == "YES":
        return "BIG PLAYER ENTRY"
    else:
        return "NO BIG PLAYER"

