"""
PHASE 11 — MASTER CENTRAL EXECUTION SWITCH
Single Command Institutional Execution Controller
"""

import logging
from datetime import datetime
from master_brain import run_master_brain

logging.basicConfig(
    filename="logs/master_execution_switch.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def run_full_system():

    logging.info("====================================================")
    logging.info("FULL SYSTEM CENTRAL EXECUTION STARTED")
    logging.info(f"Execution Time: {datetime.utcnow()} UTC")

    try:
        run_master_brain()
        logging.info("FULL SYSTEM EXECUTION COMPLETED SUCCESSFULLY")

    except Exception as e:
        logging.exception(f"CENTRAL EXECUTION FAILURE: {str(e)}")

# HARDENED: disabled main entry
    run_full_system()


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
