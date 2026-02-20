"""
ULTIMATE BRAIN
INSTITUTIONAL MASTER ORCHESTRATOR
STRICT DATA SEGREGATION MODEL
"""

import csv
import traceback
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRICE_DATA_PATH = PROJECT_ROOT / "data" / "prices"

class ExecutionState:
    INITIALIZED = "INITIALIZED"
    VALIDATED = "VALIDATED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class MasterBrain:

    def __init__(self):
        self.state = ExecutionState.INITIALIZED
        self.market_data = []
        self.symbol_snapshot = {}

    # -------------------------------------
    # ENVIRONMENT VALIDATION
    # -------------------------------------
    def validate_environment(self):

        if not PRICE_DATA_PATH.exists():
            raise RuntimeError("CRITICAL: data/prices folder missing")

        self.state = ExecutionState.VALIDATED

    # -------------------------------------
    # SAFE EXECUTION
    # -------------------------------------
    def safe_execute(self, func, name):
        try:
            return func()
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"PIPELINE FAILURE in {name} -> {str(e)}")

    # -------------------------------------
    # LOAD ONLY PRICE FILES
    # -------------------------------------
    def load_market_data(self):

        files = list(PRICE_DATA_PATH.glob("*.csv"))

        if not files:
            raise RuntimeError("No price CSV files found in data/prices/")

        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                if reader.fieldnames != ["date", "symbol", "price"]:
                    raise RuntimeError(
                        f"Invalid price schema in {file.name} | Expected: date,symbol,price"
                    )

                for row in reader:
                    self.market_data.append(row)

        if not self.market_data:
            raise RuntimeError("Market data empty after load")

    # -------------------------------------
    # SIMPLE SNAPSHOT ENGINE
    # -------------------------------------
    def run_intelligence_layer(self):

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

    # -------------------------------------
    # OUTPUT
    # -------------------------------------
    def build_structured_output(self):

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "rows_loaded": len(self.market_data),
            "symbols_processed": len(self.symbol_snapshot),
            "status": "INSTITUTIONAL_PIPELINE_ACTIVE"
        }

    # -------------------------------------
    # EXECUTION
    # -------------------------------------
    def execute(self):

        if self.state != ExecutionState.VALIDATED:
            raise RuntimeError("System not validated")

        self.safe_execute(self.load_market_data, "Load Market Data")
        self.safe_execute(self.run_intelligence_layer, "Run Intelligence Layer")

        return self.safe_execute(
            self.build_structured_output,
            "Build Structured Output"
        )


if __name__ == "__main__":
    brain = MasterBrain()
    brain.validate_environment()
    result = brain.execute()
    print(result)
