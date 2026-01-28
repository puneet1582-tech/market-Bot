import requests

API_KEY = "YOUR_API_KEY_HERE"

SECTOR_KEYWORDS = {
    "Energy": ["oil", "gas", "energy", "opec"],
    "IT": ["tech", "software", "ai", "chip"],
    "Finance": ["bank", "loan", "interest rate", "fed"],
    "Micro": ["smallcap", "startup"]
}

def fetch_global_news():
    url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    return data.get("articles", [])

def analyze_global_news(articles):
    impact = {"Energy": 0, "IT": 0, "Finance": 0, "Micro": 0}

    for art in articles:
        text = (art.get("title","") + " " + str(art.get("description",""))).lower()
        for sector, keys in SECTOR_KEYWORDS.items():
            for k in keys:
                if k in text:
                    if "rise" in text or "up" in text or "positive" in text:
                        impact[sector] += 1
                    elif "fall" in text or "down" in text or "negative" in text:
                        impact[sector] -= 1
    return impact

def sector_global_signal(sector, impact):
    val = impact.get(sector, 0)
    if val > 0:
        return "GLOBAL POSITIVE"
    elif val < 0:
        return "GLOBAL NEGATIVE"
    else:
        return "GLOBAL NEUTRAL"
