"""
ULTIMATE BRAIN
INSTITUTIONAL MASTER ORCHESTRATOR (STEP-M)
PRICE + FUNDAMENTAL + MODE READY ARCHITECTURE
STRICT PIPELINE CONTROL
"""

import csv
import traceback
from pathlib import Path
from datetime import datetime
from core.data_ingestion_engine import DataIngestionEngine
from core.fundamental_engine import FundamentalEngine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRICE_DATA_PATH = PROJECT_ROOT / "data" / "prices"


class MasterBrain:

    def __init__(self):
        self.market_data = []
        self.symbol_snapshot = {}
        self.market_mode = "UNDEFINED"

        self.ingestion = DataIngestionEngine()
        self.fundamental_engine = FundamentalEngine()

    # -------------------------------------------------
    # PHASE 1: ENVIRONMENT VALIDATION
    # -------------------------------------------------

    def validate_environment(self):
        self.ingestion.ensure_data_ready()

    # -------------------------------------------------
    # SAFE EXECUTION WRAPPER
    # -------------------------------------------------

    def safe_execute(self, func, name):
        try:
            return func()
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"PIPELINE FAILURE in {name} -> {str(e)}")

    # -------------------------------------------------
    # PHASE 2: MARKET MODE DETECTION (PLACEHOLDER)
    # -------------------------------------------------

    def detect_market_mode(self):
        """
        Future: Liquidity + Volatility + Narrative Based Mode Detection
        INVEST / TRADE / DEFENSIVE
        """
        self.market_mode = "UNDEFINED"
        return self.market_mode

    # -------------------------------------------------
    # PHASE 3: LOAD MARKET DATA
    # -------------------------------------------------

    def load_market_data(self):
        files = list(PRICE_DATA_PATH.glob("*.csv"))

        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.market_data.append(row)

    # -------------------------------------------------
    # PHASE 4: PRICE SNAPSHOT ENGINE
    # -------------------------------------------------

    def run_price_snapshot(self):
        for row in self.market_data:
            symbol = row["symbol"]
            date = row["date"]
            price = float(row["price"])

            if symbol not in self.symbol_snapshot:
                self.symbol_snapshot[symbol] = (date, price)
            else:
                if date > self.symbol_snapshot[symbol][0]:
                    self.symbol_snapshot[symbol] = (date, price)

        self.symbol_snapshot = {
            k: v[1] for k, v in self.symbol_snapshot.items()
        }

    # -------------------------------------------------
    # PHASE 5: FUNDAMENTAL ENGINE
    # -------------------------------------------------

    def run_fundamental_engine(self):
        self.fundamental_engine.load_data()
        return self.fundamental_engine.run()

    # -------------------------------------------------
    # MASTER EXECUTION PIPELINE
    # -------------------------------------------------

    def execute(self):

        # Phase 1
        self.safe_execute(self.validate_environment, "Environment Validation")

        # Phase 2
        self.safe_execute(self.detect_market_mode, "Market Mode Detection")

        # Phase 3
        self.safe_execute(self.load_market_data, "Load Market Data")

        # Phase 4
        self.safe_execute(self.run_price_snapshot, "Price Snapshot Engine")

        # Phase 5
        fundamental_results = self.safe_execute(
            self.run_fundamental_engine,
            "Fundamental Engine"
        )

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "market_mode": self.market_mode,
            "symbols_processed": len(self.symbol_snapshot),
            "fundamental_analysis": fundamental_results
        }


if __name__ == "__main__":
    brain = MasterBrain()
    result = brain.execute()
    print(result)

