"""
Ultimate Brain — Institutional Classification Engine
Generates INVEST / TRADE / DEFENSIVE classified opportunity map
"""

class InstitutionalClassificationEngine:

    def classify(self, enriched_stocks):
        invest, trade, defensive = [], [], []

        for s in enriched_stocks:
            prob = s.get("probability_score", 50)

            if prob >= 70:
                invest.append(s)
            elif prob >= 50:
                trade.append(s)
            else:
                defensive.append(s)

        return {
            "INVEST": invest,
            "TRADE": trade,
            "DEFENSIVE": defensive
        }
