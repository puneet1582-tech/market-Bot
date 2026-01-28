import requests

API_KEY = "4c95d9dfaef14ba49fd3e5cd19b5efb7"

def fetch_live_news():
    url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    return data.get("articles", [])

def live_sector_impact(articles):
    sector_map = {
        "IT": ["tech", "software", "ai"],
        "Energy": ["oil", "gas", "energy"],
        "Finance": ["bank", "loan", "finance"],
        "Micro": ["smallcap", "startup"]
    }

    impact = {"IT": 0, "Energy": 0, "Finance": 0, "Micro": 0}

    for art in articles:
        title = art.get("title") or ""
        desc = art.get("description") or ""
        text = (title + " " + desc).lower()

        for sector, keywords in sector_map.items():
            for k in keywords:
                if k in text:
                    if "rise" in text or "up" in text or "positive" in text:
                        impact[sector] += 1
                    elif "fall" in text or "down" in text or "negative" in text:
                        impact[sector] -= 1

    return impact
