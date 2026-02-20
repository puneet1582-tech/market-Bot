import csv

def load_stocks(filepath="data/stocks.csv"):
    stocks = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stocks.append(row)
    return stocks
