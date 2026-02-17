# OPPORTUNITY REPORT ENGINE
# Generates institutional-style opportunity summary

from datetime import datetime

def generate_report(ranked_opportunities, sector_scores):
    try:
        report = {
            "timestamp": str(datetime.now()),
            "top_opportunities": ranked_opportunities[:5],
            "sector_strength": sector_scores
        }
        return report
    except Exception as e:
        print("Report generation error:", e)
        return {}
