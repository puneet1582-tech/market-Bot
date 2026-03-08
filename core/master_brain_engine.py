import sys
import os

# ensure project root in path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.intelligence_engine import IntelligenceEngine
from core.sector_engine import SectorEngine
from core.global_impact_engine import GlobalImpactEngine

# compatible import for opportunity engine
try:
    from core.opportunity_detection_engine import OpportunityDetectionEngine
except ImportError:
    from core.opportunity_detection_engine import OpportunityEngine as OpportunityDetectionEngine


class MasterBrainEngine:

    def __init__(self):
        self.intelligence_engine = IntelligenceEngine()
        self.opportunity_engine = OpportunityDetectionEngine()
        self.sector_engine = SectorEngine()
        self.global_engine = GlobalImpactEngine()

    def run(self):

        intelligence_output = self.intelligence_engine.run()
        opportunity_output = self.opportunity_engine.run()
        sector_output = self.sector_engine.run()
        global_output = self.global_engine.run()

        final_report = {
            "top_opportunities": opportunity_output,
            "sector_summary": sector_output,
            "global_impact": global_output,
            "stock_decisions": intelligence_output
        }

        print("MASTER BRAIN REPORT GENERATED")

        return final_report


def run():
    engine = MasterBrainEngine()
    result = engine.run()
    print(result)


if __name__ == "__main__":
    run()
