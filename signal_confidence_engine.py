# SIGNAL CONFIDENCE ENGINE
# Calculates confidence score for signals

def calculate_signal_confidence(conviction_ranked, persistent_list, regime_prob):
    try:
        bull = regime_prob.get("bull_probability", 0)
        bear = regime_prob.get("bear_probability", 0)

        regime_strength = max(bull, bear)

        updated = []

        for op in conviction_ranked:
            symbol = op["symbol"]
            score = op.get("conviction_score", 0)

            confidence = score * 0.6

            if symbol in persistent_list:
                confidence += 15

            confidence += regime_strength * 0.2

            op["confidence_percent"] = round(min(confidence, 100), 2)
            updated.append(op)

        return updated

    except Exception as e:
        print("Confidence calculation error:", e)
        return conviction_ranked
