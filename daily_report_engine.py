# DAILY REPORT ENGINE
# Generates structured daily intelligence report

from datetime import datetime

def generate_daily_report(dashboard):
    try:
        report_text = (
            f"DAILY MARKET INTELLIGENCE REPORT\n"
            f"Date: {datetime.now()}\n\n"
            f"Market Mode: {dashboard['market_mode']}\n"
            f"Sector Strength: {dashboard['sector_strength']}\n"
            f"Top Opportunities: {dashboard['top_opportunities']}\n"
            f"Performance Summary: {dashboard['performance_summary']}\n"
            f"Return Estimation: {dashboard['return_estimation']}\n"
        )
        return report_text
    except Exception as e:
        return f"Report generation error: {e}"
