from .business_evolution_engine import BusinessEvolutionEngine
from .institutional_behavior_engine import InstitutionalBehaviorEngine
from .sector_intelligence_engine import SectorIntelligenceEngine
from .global_macro_mapping_engine import GlobalMacroMappingEngine
from .market_mode_engine import MarketModeEngine
from .global_impact_engine import GlobalImpactEngine
from .multibagger_engine import MultibaggerEngine

class MasterIntelligenceEngine:

    def __init__(self):
        self.business = BusinessEvolutionEngine()
        self.institutional = InstitutionalBehaviorEngine()
        self.sector = SectorIntelligenceEngine()
        self.macro = GlobalMacroMappingEngine()
        self.market = MarketModeEngine()
        self.impact = GlobalImpactEngine()
        self.multibagger = MultibaggerEngine()

    def run_full_analysis(self, company_data):
        report = {}

        business = self.business.analyze(company_data.get("financials"))
        institutional = self.institutional.analyze(company_data.get("ownership"))
        sector = self.sector.analyze(company_data.get("sector"))
        macro = self.macro.analyze(company_data.get("macro"))
        market_mode = self.market.determine_mode(
            company_data.get("liquidity"),
            company_data.get("volatility")
        )

        impact = None
        if "event_type" in company_data:
            impact = self.impact.analyze_event(
                company_data.get("event_type"),
                company_data.get("sector_profile", {}),
                company_data.get("company_profile", {})
            )

        multibagger = self.multibagger.evaluate(
            business,
            institutional,
            sector,
            macro,
            impact
        )

        report["business_evolution"] = business
        report["institutional_behavior"] = institutional
        report["sector_intelligence"] = sector
        report["macro_mapping"] = macro
        report["market_mode"] = market_mode

        if impact:
            report["global_event_impact"] = impact

        report["multibagger_analysis"] = multibagger

        return report
