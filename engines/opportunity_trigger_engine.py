from engines.telegram_alert_engine import send_telegram_alert


def classify_mode(score):
    if score >= 80:
        return "INVEST"
    elif score >= 60:
        return "TRADE"
    else:
        return "DEFENSIVE"


def process_opportunity(stock_symbol, analysis_result, market_mode="TRADE"):
    """
    analysis_result expected:
    {
        "score": 0-100,
        "summary": "text"
    }
    """

    score = analysis_result.get("score", 0)
    summary = analysis_result.get("summary", "No summary available")

    signal_mode = classify_mode(score)

    # Mode-aware filtering
    trigger_threshold = 70
    if market_mode == "DEFENSIVE":
        trigger_threshold = 85
    elif market_mode == "INVEST":
        trigger_threshold = 65

    if score >= trigger_threshold:
        message = (
            f"MODE: {market_mode}\n"
            f"OPPORTUNITY ALERT\n"
            f"Stock: {stock_symbol}\n"
            f"Signal Type: {signal_mode}\n"
            f"Score: {score}\n"
            f"{summary}"
        )
        send_telegram_alert(message)

    return signal_mode
