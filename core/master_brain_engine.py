"""
ULTIMATE BRAIN
MASTER BRAIN UNIFIED REPORT ENGINE
All Layers Integrated
"""

from core.intelligence_engine import IntelligenceEngine
from core.opportunity_engine import OpportunityEngine
from core.sector_engine import SectorEngine
from core.global_impact_engine import GlobalImpactEngine


class MasterBrainEngine:

    def __init__(self):
        self.intelligence_engine = IntelligenceEngine()
        self.opportunity_engine = OpportunityEngine()
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

        return final_report


if __name__ == "__main__":
    engine = MasterBrainEngine()
    result = engine.run()
    print("MASTER BRAIN REPORT GENERATED")
    print(result)
