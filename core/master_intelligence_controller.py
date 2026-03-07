from market_brain import run_market_brain
from fundamental_brain import run_fundamental_analysis
from quarterly_comparison_engine import run_quarterly_analysis
from sector_intelligence_engine import run_sector_intelligence
from global_event_engine import run_global_event_analysis
from opportunity_engine import generate_top_opportunities


class MasterIntelligenceController:

    def execute(self):

        print("Running Market Brain")
        run_market_brain()

        print("Running Fundamental Analysis")
        run_fundamental_analysis()

        print("Running Quarterly Comparison")
        run_quarterly_analysis()

        print("Running Sector Intelligence")
        run_sector_intelligence()

        print("Running Global Event Intelligence")
        run_global_event_analysis()

        print("Generating Opportunities")
        top = generate_top_opportunities()

        result = {
            "MARKET_SUMMARY": {
                "mode": "ACTIVE"
            },
            "TOP_20": top
        }

        return result
