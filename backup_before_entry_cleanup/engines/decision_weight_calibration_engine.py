"""
Ultimate Brain — Decision Weight Calibration Engine
Adjusts internal scoring weights dynamically based on evolution signals.
"""

class DecisionWeightCalibrationEngine:

    def calibrate(self, dashboard):
        evo = dashboard.get("strategy_evolution_signal", {})

        weights = {
            "invest_weight": 1.0,
            "trade_weight": 1.0,
            "defensive_weight": 1.0
        }

        if evo.get("invest_bias_adjustment"):
            weights["invest_weight"] *= 1.1
        if evo.get("trade_bias_adjustment"):
            weights["trade_weight"] *= 1.05
        if evo.get("defensive_bias_adjustment"):
            weights["defensive_weight"] *= 1.1

        return weights
