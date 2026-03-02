import requests
import json
import feedparser
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_stooq(symbol):
    try:
        url = f"https://stooq.com/q/l/?s={symbol}&f=sd2t2ohlcv&h&e=csv"
        r = requests.get(url, timeout=10)
        lines = r.text.split("\n")
        if len(lines) > 1:
            parts = lines[1].split(",")
            if len(parts) > 6:
                return parts[6]
    except:
        return None
    return None

def fetch_news():
    feed = feedparser.parse("https://feeds.reuters.com/reuters/topNews")
    headlines = [e.title.lower() for e in feed.entries[:10]]
    return headlines

def war_score(news):
    keywords = ["war","missile","attack","conflict","iran","israel"]
    score = 0
    for n in news:
        for k in keywords:
            if k in n:
                score += 1
    return score

def sector_model(score):
    if score >= 3:
        return {
            "Oil": 80,
            "Gold": 70,
            "Defense": 65,
            "Aviation": -60
        }
    elif score >= 1:
        return {
            "Oil": 55,
            "Gold": 50,
            "Defense": 40,
            "Aviation": -30
        }
    return {}

def run():
    data = {}
    data["timestamp"] = str(datetime.utcnow())
    data["oil"] = fetch_stooq("cl.f")
    data["spx"] = fetch_stooq("^spx")
    data["reliance"] = fetch_stooq("reliance.ns")
    news = fetch_news()
    score = war_score(news)
    data["war_score"] = score
    data["sector_probabilities"] = sector_model(score)

    with open("live_data.json", "w") as f:
        json.dump(data, f, indent=4)

    print("INTELLIGENCE UPDATED")

if __name__ == "__main__":
    run()
