# DAILY REPORT ENGINE
# Hindi report with English stock names

from datetime import datetime

def generate_daily_report(dashboard):
    try:
        top_stocks = [op["symbol"] for op in dashboard["top_opportunities"]]

        report_text = (
            f"दैनिक मार्केट इंटेलिजेंस रिपोर्ट\n"
            f"तारीख: {datetime.now()}\n\n"
            f"मार्केट मोड: {dashboard['market_mode']['mode']}\n"
            f"मजबूत सेक्टर: {dashboard['sector_strength']}\n"
            f"टॉप अवसर (Stocks): {', '.join(top_stocks)}\n"
            f"परफॉर्मेंस सारांश: {dashboard['performance_summary']}\n"
            f"रिटर्न अनुमान: {dashboard['return_estimation']}\n"
        )

        return report_text

    except Exception as e:
        return f"Report error: {e}"
