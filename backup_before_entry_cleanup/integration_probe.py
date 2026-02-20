"""
INTEGRATION PROBE
Scans all critical orchestration imports and reports failures
"""

modules = [
    "master_brain",
    "engines.global_intelligence_integration",
    "engines.global_news_engine",
    "engines.global_sector_stock_map_engine",
    "engines.global_signal_fusion_engine",
    "engines.intelligence_orchestrator_engine",
    "engines.unified_daily_decision_engine",
    "engines.master_brain_controller_engine",
    "engines.autonomous_daily_runner"
]

for m in modules:
    try:
        __import__(m)
        print(f"[OK] {m}")
    except Exception as e:
        print(f"[ERROR] {m} -> {e}")
