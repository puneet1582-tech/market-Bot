"""
Ultimate Brain — Global News → Sector → Stock Impact Scoring Engine
Production-ready base for sentiment-driven sector intelligence
"""

from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

SECTOR_KEYWORDS = {
    "IT": ["software", "tech", "ai", "cloud"],
    "BANKING": ["bank", "credit", "loan", "interest rate"],
    "ENERGY": ["oil", "gas", "energy"],
    "FMCG": ["consumer", "retail", "fmcg"]
}


def detect_sector(text):
    text_lower = text.lower()
    sectors = []
    for s, kws in SECTOR_KEYWORDS.items():
        if any(k in text_lower for k in kws):
            sectors.append(s)
    return sectors


def analyze_news(news_list):
    results = []
    for n in news_list:
        text = n.get("title", "") + " " + n.get("description", "")
        sentiment = analyzer.polarity_scores(text)["compound"]
        sectors = detect_sector(text)

        results.append({
            "timestamp": str(datetime.utcnow()),
            "headline": n.get("title"),
            "sentiment_score": sentiment,
            "impacted_sectors": sectors
        })

    return results
