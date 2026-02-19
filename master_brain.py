"""
MASTER BRAIN — CORE INTELLIGENCE ORCHESTRATOR
Institutional Grade Central Execution Brain
"""

import logging
from datetime import datetime

# Core Intelligence Engines
from engines.global_intelligence_integration import run_global_intelligence
from engines.intelligence_orchestrator_engine import run_intelligence_orchestrator
from engines.unified_daily_decision_engine import run_unified_daily_decision
from engines.master_brain_controller_engine import run_master_brain_controller
from engines.autonomous_daily_runner import run_autonomous_daily_cycle

# NEW PHASE-2 ENGINE
from engines.sector_money_flow_engine import run_sector_money_flow_engine

logging.basicConfig(
    filename="logs/master_brain.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def run_master_brain():

    logging.info("===================================================")
    logging.info("MASTER BRAIN EXECUTION STARTED")
    logging.info(f"Execution Time: {datetime.now()}")

    logging.info("STEP 1: Global Intelligence Integration")
    run_global_intelligence()

    logging.info("STEP 2: Intelligence Orchestrator Execution")
    run_intelligence_orchestrator()

    logging.info("STEP 3: Unified Daily Decision Engine")
    run_unified_daily_decision()

    logging.info("STEP 4: Sector Money Flow Intelligence")
    run_sector_money_flow_engine()

    logging.info("STEP 5: Master Brain Controller")
    run_master_brain_controller()

    logging.info("STEP 6: Autonomous Daily Execution Cycle")
    run_autonomous_daily_cycle()

    logging.info("MASTER BRAIN EXECUTION COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    run_master_brain()
