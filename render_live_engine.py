import requests
import os
import json
import time
import feedparser
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HEADERS = {"User-Agent": "Mozilla/5.0"}

CACHE_FILE = "live_market_cache.json"

WAR_KEYWORDS = ["war","attack","missile","iran","israel","us strike","conflict"]

SECTOR_MAP = {
    "Oil": ["CL=F"],
    "Gold": ["GC=F"],
    "US Index": ["^GSPC"]
}

def yahoo_quote(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()
        price = data["quoteResponse"]["result"][0]["regularMarketPrice"]
        return price
    except:
        return None

def stooq_fallback(symbol):
    try:
        url = f"https://stooq.com/q/l/?s={symbol.lower()}&f=sd2t2ohlcv&h&e=csv"
        r = requests.get(url, timeout=10)
        lines = r.text.split("\n")
        if len(lines) > 1:
            return float(lines[1].split(",")[6])
    except:
        return None

def get_price(symbol):
    p = yahoo_quote(symbol)
    if p:
        return p
    return stooq_fallback(symbol)

def fetch_news():
    feed = feedparser.parse("https://feeds.reuters.com/reuters/topNews")
    headlines = []
    for entry in feed.entries[:10]:
        headlines.append(entry.title.lower())
    return headlines

def war_signal(news_list):
    score = 0
    for n in news_list:
        for k in WAR_KEYWORDS:
            if k in n:
                score += 1
    return score

def sector_probability(war_score):
    if war_score >= 3:
        return {
            "Oil": 80,
            "Gold": 75,
            "Aviation": -70,
            "Defense": 65
        }
    elif war_score == 2:
        return {
            "Oil": 60,
            "Gold": 55,
            "Aviation": -40,
            "Defense": 45
        }
    else:
        return {}

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})

def run_engine():
    report = {}
    report["timestamp"] = str(datetime.utcnow())

    oil = get_price("CL=F")
    gold = get_price("GC=F")
    spx = get_price("^GSPC")

    report["commodities"] = {"Oil": oil, "Gold": gold}
    report["index"] = {"SP500": spx}

    news = fetch_news()
    war_score = war_signal(news)

    probabilities = sector_probability(war_score)
    report["war_score"] = war_score
    report["sector_probabilities"] = probabilities

    with open(CACHE_FILE, "w") as f:
        json.dump(report, f, indent=4)

    if probabilities:
        msg = f"⚠ WAR SIGNAL DETECTED\nScore: {war_score}\n{probabilities}"
        send_telegram(msg)

    print("LIVE ENGINE RUN COMPLETE")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    run_engine()
