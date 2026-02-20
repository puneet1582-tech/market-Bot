# STRATEGY REGIME SWITCH ENGINE
# Adjusts strategic bias based on regime probabilities

def adjust_strategy_bias(mode_report, regime_prob):
    try:
        bull = regime_prob.get("bull_probability", 0)
        bear = regime_prob.get("bear_probability", 0)

        adjusted_mode = mode_report.get("mode", "TRADE")

        if bull > 55:
            adjusted_mode = "INVEST"
        elif bear > 55:
            adjusted_mode = "DEFENSIVE"
        else:
            adjusted_mode = "TRADE"

        return {
            "mode": adjusted_mode,
            "original_mode": mode_report.get("mode", "TRADE")
        }

    except Exception as e:
        print("Strategy switch error:", e)
        return mode_report
