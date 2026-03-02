from .business_evolution_engine import BusinessEvolutionEngine
from .institutional_behavior_engine import InstitutionalBehaviorEngine
from .sector_intelligence_engine import SectorIntelligenceEngine
from .global_macro_mapping_engine import GlobalMacroMappingEngine
from .market_mode_engine import MarketModeEngine
from .global_impact_engine import GlobalImpactEngine

class MasterIntelligenceEngine:

    def __init__(self):
        self.business = BusinessEvolutionEngine()
        self.institutional = InstitutionalBehaviorEngine()
        self.sector = SectorIntelligenceEngine()
        self.macro = GlobalMacroMappingEngine()
        self.market = MarketModeEngine()
        self.impact = GlobalImpactEngine()

    def run_full_analysis(self, company_data):
        report = {}

        report["business_evolution"] = self.business.analyze(company_data.get("financials"))
        report["institutional_behavior"] = self.institutional.analyze(company_data.get("ownership"))
        report["sector_intelligence"] = self.sector.analyze(company_data.get("sector"))
        report["macro_mapping"] = self.macro.analyze(company_data.get("macro"))
        report["market_mode"] = self.market.determine_mode(
            company_data.get("liquidity"),
            company_data.get("volatility")
        )

        if "event_type" in company_data:
            report["global_event_impact"] = self.impact.analyze_event(
                company_data.get("event_type"),
                company_data.get("sector_profile", {}),
                company_data.get("company_profile", {})
            )

        return report
