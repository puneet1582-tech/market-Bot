"""
Ultimate Brain — Intelligence Orchestrator
Combines regime, sector, opportunity, probability, and narrative layers
"""

from engines.global_intelligence_engine import GlobalIntelligenceEngine
from engines.probability_intelligence_engine import ProbabilityIntelligenceEngine
from engines.scenario_simulation_engine import ScenarioSimulationEngine


class IntelligenceOrchestrator:

    def __init__(self):
        self.global_engine = GlobalIntelligenceEngine()
        self.prob_engine = ProbabilityIntelligenceEngine()
        self.scenario_engine = ScenarioSimulationEngine()

    def run(self, conviction_list, regime_score, sector_strength, volatility):
        global_snapshot = self.global_engine.generate_snapshot()

        enriched = []
        for stock in conviction_list:
            prob = self.prob_engine.compute_probability(
                stock.get("conviction_score", 50),
                regime_score,
                sector_strength.get(stock.get("sector"), 50)
            )

            scenario_prob = self.scenario_engine.simulate(prob, volatility)

            stock["probability_score"] = scenario_prob
            enriched.append(stock)

        return {
            "snapshot": global_snapshot,
            "stocks": enriched
        }
