import sys
import os

# Ensure project root is always in Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

"""
ULTIMATE BRAIN
MASTER BRAIN UNIFIED REPORT ENGINE
Institutional Grade Orchestration Layer
"""

from core.intelligence_engine import IntelligenceEngine
from core.opportunity_detection_engine import OpportunityDetectionEngine
from core.sector_engine import SectorEngine
from core.global_impact_engine import GlobalImpactEngine


class MasterBrainEngine:

    def __init__(self):

        self.intelligence_engine = IntelligenceEngine()
        self.opportunity_engine = OpportunityDetectionEngine()
        self.sector_engine = SectorEngine()
        self.global_engine = GlobalImpactEngine()

    def run(self):

        intelligence_output = None
        opportunity_output = None
        sector_output = None
        global_output = None

        try:
            intelligence_output = self.intelligence_engine.run()
        except Exception as e:
            print("Intelligence Engine Error:", e)

        try:
            opportunity_output = self.opportunity_engine.run()
        except Exception as e:
            print("Opportunity Engine Error:", e)

        try:
            sector_output = self.sector_engine.run()
        except Exception as e:
            print("Sector Engine Error:", e)

        try:
            global_output = self.global_engine.run()
        except Exception as e:
            print("Global Impact Engine Error:", e)

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

