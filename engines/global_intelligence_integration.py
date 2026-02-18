"""
GLOBAL INTELLIGENCE INTEGRATION ENGINE
Compatibility Wrapper for Master Brain Execution
"""

import logging

from engines.global_news_engine import run_global_news_engine
from engines.global_sector_stock_map_engine import run_global_sector_stock_mapping
from engines.global_signal_fusion_engine import run_global_signal_fusion

logging.basicConfig(level=logging.INFO)

def run_global_intelligence():
    """
    Master Brain compatible global intelligence execution
    """

    logging.info("GLOBAL INTELLIGENCE EXECUTION STARTED")

    try:
        run_global_news_engine()
    except Exception as e:
        logging.warning(f"Global News Engine skipped: {e}")

    try:
        run_global_sector_stock_mapping()
    except Exception as e:
        logging.warning(f"Sector Stock Mapping skipped: {e}")

    try:
        run_global_signal_fusion()
    except Exception as e:
        logging.warning(f"Global Signal Fusion skipped: {e}")

    logging.info("GLOBAL INTELLIGENCE EXECUTION COMPLETED")
