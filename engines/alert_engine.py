from engines.trading_brain_engine import TradingBrainEngine
from engines.time_mode_engine import TimeModeEngine

class AlertEngine:
    def __init__(self):
        self.trading_brain = TradingBrainEngine()
        self.time_engine = TimeModeEngine()

    def check_alert(self):
        trade_result = self.trading_brain.decide_trade()

        if trade_result["decision"] != "TRADE":
            return {
                "alert": False,
                "reason": trade_result["why"]
            }

        market_mode = trade_result["market_mode"]

        time_ok, time_reason = self.time_engine.is_trade_time(market_mode)

        if not time_ok:
            return {
                "alert": False,
                "reason": time_reason
            }

        return {
            "alert": True,
            "message": "READY – TRADE OPPORTUNITY",
            "details": trade_result
        }
