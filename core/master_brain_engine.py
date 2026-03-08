"""
ULTIMATE BRAIN
MASTER BRAIN UNIFIED REPORT ENGINE
Institutional Grade Orchestration Layer
All Intelligence Layers Integrated
"""

from core.intelligence_engine import IntelligenceEngine
from core.opportunity_detection_engine import OpportunityDetectionEngine
from core.sector_engine import SectorEngine
from core.global_impact_engine import GlobalImpactEngine
from core.system_logger import get_logger


class MasterBrainEngine:
    """
    Central orchestration engine of Ultimate Brain.
    Combines intelligence, sector analysis, global impact,
    and opportunity detection into a unified decision report.
    """

    def __init__(self):

        self.logger = get_logger("MASTER_BRAIN")

        self.intelligence_engine = IntelligenceEngine()
        self.opportunity_engine = OpportunityDetectionEngine()
        self.sector_engine = SectorEngine()
        self.global_engine = GlobalImpactEngine()

    def run(self):

        self.logger.info("MASTER BRAIN EXECUTION STARTED")

        try:

            intelligence_output = self.intelligence_engine.run()
            self.logger.info("Intelligence layer completed")

            opportunity_output = self.opportunity_engine.run()
            self.logger.info("Opportunity detection completed")

            sector_output = self.sector_engine.run()
            self.logger.info("Sector analysis completed")

            global_output = self.global_engine.run()
            self.logger.info("Global impact analysis completed")

            final_report = {
                "top_opportunities": opportunity_output,
                "sector_summary": sector_output,
                "global_impact": global_output,
                "stock_decisions": intelligence_output
            }

            self.logger.info("MASTER BRAIN REPORT GENERATED")

            return final_report

        except Exception as e:

            self.logger.error(f"MASTER BRAIN FAILURE: {e}")

            raise


def run():

    engine = MasterBrainEngine()

    report = engine.run()

    print("MASTER BRAIN REPORT GENERATED")

    if isinstance(report, dict):
        for key in report:
            print(f"{key} -> generated")

    return report


if __name__ == "__main__":

    run()

