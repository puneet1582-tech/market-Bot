from engines.opportunity_engine import generate_top_opportunities

class MasterIntelligenceController:

    def execute(self):

        market_mode = "TRADE"

        top = generate_top_opportunities()

        result = {
            "MARKET_SUMMARY": {
                "mode": market_mode
            },
            "TOP_20": top
        }

        return result
