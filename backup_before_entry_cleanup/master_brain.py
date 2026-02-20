import logging
from datetime import datetime

from engines.global_intelligence_integration import run_global_intelligence
from engines.intelligence_orchestrator_engine import run_intelligence_orchestrator
from engines.sector_money_flow_engine import run_sector_money_flow_engine
from engines.unified_daily_decision_engine import run_unified_daily_decision
from engines.master_brain_controller_engine import run_master_brain_controller
from engines.autonomous_daily_runner import run_autonomous_daily_cycle


def run_master_brain():

    logging.basicConfig(level=logging.INFO)

    logging.info("===================================================")
    logging.info("MASTER BRAIN EXECUTION STARTED")
    logging.info(f"Execution Time: {datetime.now()}")

    logging.info("STEP 1: Global Intelligence Integration")
    run_global_intelligence()

    logging.info("STEP 2: Intelligence Orchestrator Execution")
    run_intelligence_orchestrator()

    logging.info("STEP 3: Sector Money Flow Intelligence")
    run_sector_money_flow_engine()

    logging.info("STEP 4: Unified Daily Decision Engine")
    run_unified_daily_decision()

    logging.info("STEP 5: Master Brain Controller")
    run_master_brain_controller()

    logging.info("STEP 6: Autonomous Daily Runner")
    run_autonomous_daily_cycle()

    logging.info("MASTER BRAIN EXECUTION COMPLETED")
