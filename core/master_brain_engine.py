import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.intelligence_engine import IntelligenceEngine
from core.opportunity_detection_engine import OpportunityDetectionEngine
from core.sector_engine import SectorEngine
from core.global_impact_engine import GlobalImpactEngine
from core.multibagger_detection_engine import MultibaggerDetectionEngine
from core.business_quality_engine import BusinessQualityEngine
from core.institutional_flow_engine import InstitutionalFlowEngine
from core.mode_engine import MarketModeEngine


class MasterBrainEngine:

    def __init__(self):

        self.intelligence_engine = IntelligenceEngine()
        self.opportunity_engine = OpportunityDetectionEngine()
        self.sector_engine = SectorEngine()
        self.global_engine = GlobalImpactEngine()
        self.multibagger_engine = MultibaggerDetectionEngine()
        self.business_engine = BusinessQualityEngine()
        self.institutional_engine = InstitutionalFlowEngine()
        self.market_mode_engine = MarketModeEngine()

    def run(self):

        print("MASTER BRAIN EXECUTION STARTED")

        intelligence_output = self.intelligence_engine.run()
        opportunity_output = self.opportunity_engine.run()
        sector_output = self.sector_engine.run()
        global_output = self.global_engine.run()
        multibagger_output = self.multibagger_engine.run()
        business_output = self.business_engine.run()
        institutional_output = self.institutional_engine.run()
        market_mode_output = self.market_mode_engine.run()

        final_report = {
            "market_mode": market_mode_output,
            "top_opportunities": opportunity_output,
            "multibagger_candidates": multibagger_output,
            "business_quality": business_output,
            "institutional_flow": institutional_output,
            "sector_summary": sector_output,
            "global_impact": global_output,
            "system_intelligence": intelligence_output
        }

        print("MASTER BRAIN REPORT GENERATED")

        return final_report


def run():

    engine = MasterBrainEngine()

    result = engine.run()

    print(result)


if __name__ == "__main__":
    run()
