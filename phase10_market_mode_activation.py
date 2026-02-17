from engines.autonomous_market_mode_controller import AutonomousMarketModeController

_engine = AutonomousMarketModeController()

def apply_market_mode_controller(dashboard):
    try:
        dashboard["autonomous_market_mode_map"] = _engine.build_market_map(dashboard)
    except Exception as e:
        dashboard["market_mode_controller_error"] = str(e)

    return dashboard
