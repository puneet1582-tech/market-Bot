from engines.master_brain_controller_engine import MasterBrainController

_controller = MasterBrainController()

def apply_master_controller(dashboard):
    try:
        dashboard["master_brain_controller"] = _controller.evaluate_system(dashboard)
    except Exception as e:
        dashboard["master_controller_error"] = str(e)

    return dashboard
