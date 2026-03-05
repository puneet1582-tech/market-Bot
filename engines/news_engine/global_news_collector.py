import json
import feedparser
from datetime import datetime, UTC

RSS_FEEDS = [
    "https://www.reuters.com/rssFeed/worldNews",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://feeds.bbci.co.uk/news/business/rss.xml"
]

OUTPUT_FILE = "data/news/global_news.json"

def collect_news():
    news_list = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:20]:
            news = {
                "headline": entry.title,
                "link": entry.link,
                "source": url,
                "timestamp": str(datetime.now(UTC))
            }

            news_list.append(news)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(news_list, f, indent=2)

    print("Global news collected:", len(news_list))

if __name__ == "__main__":
    collect_news()
