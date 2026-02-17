"""
Ultimate Brain — Autonomous Market Mode Controller
Produces a complete INVEST / TRADE / DEFENSIVE market-wide classification
using classification, strategy signals, and global macro bias.
"""

class AutonomousMarketModeController:

    def build_market_map(self, dashboard):
        classification = dashboard.get("market_mode_classification", {})
        macro_bias = dashboard.get("global_master_signal", {}).get("macro_bias", "NEUTRAL")

        market_map = {
            "macro_bias": macro_bias,
            "INVEST": classification.get("INVEST", []),
            "TRADE": classification.get("TRADE", []),
            "DEFENSIVE": classification.get("DEFENSIVE", [])
        }

        return market_map
