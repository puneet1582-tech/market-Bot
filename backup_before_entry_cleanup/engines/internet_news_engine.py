import csv

def load_internet_news(filepath="data/internet_news.csv"):
    news = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            news.append(row)
    return news

def internet_sector_impact(news_list):
    impact = {}
    for n in news_list:
        sector = n["sector"]
        sign = n["impact"]

        if sector not in impact:
            impact[sector] = 0

        if sign == "POSITIVE":
            impact[sector] += 1
        elif sign == "NEGATIVE":
            impact[sector] -= 1

    return impact

