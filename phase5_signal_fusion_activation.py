from engines.global_signal_fusion_engine import GlobalSignalFusionEngine

_fusion_engine = GlobalSignalFusionEngine()

def apply_global_signal_fusion(dashboard):
    try:
        dashboard["global_master_signal"] = _fusion_engine.fuse(dashboard)
    except Exception as e:
        dashboard["fusion_error"] = str(e)

    return dashboard
