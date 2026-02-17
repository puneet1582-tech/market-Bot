"""
Ultimate Brain — Scenario Simulation Engine
Performs forward-looking volatility-based outcome simulations
"""

class ScenarioSimulationEngine:

    def simulate(self, base_probability, volatility):
        if volatility > 30:
            return round(base_probability * 0.75, 2)
        elif volatility < 15:
            return round(base_probability * 1.15, 2)
        return base_probability
