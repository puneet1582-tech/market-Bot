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

logging.basicConfig(
    filename="logs/master_brain.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def run_master_brain():

    logging.info("===================================================")
    logging.info("MASTER BRAIN EXECUTION STARTED")
    logging.info(f"Execution Time: {datetime.utcnow()} UTC")

    try:

        logging.info("STEP 1: Global Intelligence Integration")
        run_global_intelligence()

        logging.info("STEP 2: Intelligence Orchestrator Execution")
        run_intelligence_orchestrator()

        logging.info("STEP 3: Unified Daily Decision Engine")
        run_unified_daily_decision()

        logging.info("STEP 4: Master Brain Controller")
        run_master_brain_controller()

        logging.info("STEP 5: Autonomous Daily Execution Cycle")
        run_autonomous_daily_cycle()

        logging.info("MASTER BRAIN EXECUTION COMPLETED SUCCESSFULLY")

    except Exception as e:
        logging.exception(f"MASTER BRAIN FAILURE: {str(e)}")


if __name__ == "__main__":
    run_master_brain()
