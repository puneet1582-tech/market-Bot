def news_future_signal(row):
    """
    Combines news sentiment and future sector strength.
    Safe, simple logic.
    """

    news_score = row.get("news_score", 0)
    future_score = row.get("future_score", 0)

    total = news_score + future_score

    if total >= 70:
        return "STRONG_POSITIVE"

    if total >= 40:
        return "POSITIVE"

    if total <= -30:
        return "NEGATIVE"

    return "NEUTRAL"



if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
