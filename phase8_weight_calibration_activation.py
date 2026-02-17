from engines.decision_weight_calibration_engine import DecisionWeightCalibrationEngine

_engine = DecisionWeightCalibrationEngine()

def apply_weight_calibration(dashboard):
    try:
        dashboard["decision_weight_calibration"] = _engine.calibrate(dashboard)
    except Exception as e:
        dashboard["weight_calibration_error"] = str(e)

    return dashboard
