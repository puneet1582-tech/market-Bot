"""
Ultimate Brain — Daily Top-20 Institutional Opportunity Engine
Generates daily Top-20 opportunity list from institutional opportunity scores.
"""

import pandas as pd
from datetime import datetime

INPUT_FILE = "data/institutional_opportunity_scores.csv"
OUTPUT_FILE = "data/daily_top20_opportunities.csv"


def generate_top20():
    try:
        df = pd.read_csv(INPUT_FILE)
        df = df.sort_values(by="institutional_score", ascending=False)

        top20 = df.head(20)
        top20["generated_at"] = str(datetime.utcnow())

        top20.to_csv(OUTPUT_FILE, index=False)

        return {
            "timestamp": str(datetime.utcnow()),
            "top20_count": len(top20)
        }
    except Exception as e:
        return {
            "timestamp": str(datetime.utcnow()),
            "error": str(e)
        }


if __name__ == "__main__":
    print(generate_top20())
