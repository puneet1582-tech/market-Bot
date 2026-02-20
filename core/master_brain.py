"""
ULTIMATE BRAIN
INSTITUTIONAL MASTER ORCHESTRATOR
PHASE-A REAL ENGINE WIRING
"""

import csv
import traceback
from pathlib import Path
from datetime import datetime
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data"

class ExecutionState:
    INITIALIZED = "INITIALIZED"
    VALIDATED = "VALIDATED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class MasterBrain:

    def __init__(self):
        self.state = ExecutionState.INITIALIZED
        self.pipeline_log = []
        self.market_data = []

    # ------------------------------
    # ENVIRONMENT VALIDATION
    # ------------------------------
    def validate_environment(self):

        required_files = ["run.py", "brain_control.py"]
        for file in required_files:
            if not (PROJECT_ROOT / file).exists():
                raise RuntimeError(f"CRITICAL FILE MISSING: {file}")

        if not DATA_PATH.exists():
            raise RuntimeError("CRITICAL: data/ folder missing")

        self.state = ExecutionState.VALIDATED
        self.pipeline_log.append("Environment validated")

    # ------------------------------
    # SAFE EXECUTION WRAPPER
    # ------------------------------
    def safe_execute(self, func, name):
        try:
            self.pipeline_log.append(f"START: {name}")
            result = func()
            self.pipeline_log.append(f"SUCCESS: {name}")
            return result
        except Exception as e:
            self.state = ExecutionState.FAILED
            traceback.print_exc()
            raise RuntimeError(f"PIPELINE FAILURE in {name} -> {str(e)}")

    # ------------------------------
    # LOAD PRICE DATA (LONG FORMAT)
    # ------------------------------
    def load_market_data(self):

        files = list(DATA_PATH.glob("*.csv"))
        if not files:
            raise RuntimeError("No CSV files found in data/")

        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames != ["date", "symbol", "price"]:
                    raise RuntimeError(f"Invalid schema in {file.name}")

                for row in reader:
                    self.market_data.append(row)

        if not self.market_data:
            raise RuntimeError("Market data empty after load")

        return f"{len(self.market_data)} rows loaded"

    # ------------------------------
    # BASIC INSTITUTIONAL AGGREGATION
    # ------------------------------
    def run_intelligence_layer(self):

        symbol_latest_price = {}

        for row in self.market_data:
            symbol = row["symbol"]
            date = row["date"]
            price = float(row["price"])

            if symbol not in symbol_latest_price:
                symbol_latest_price[symbol] = (date, price)
            else:
                if date > symbol_latest_price[symbol][0]:
                    symbol_latest_price[symbol] = (date, price)

        self.symbol_snapshot = {
            k: v[1] for k, v in symbol_latest_price.items()
        }

        return f"{len(self.symbol_snapshot)} symbols processed"

    # ------------------------------
    # STRUCTURED INSTITUTIONAL OUTPUT
    # ------------------------------
    def build_structured_output(self):

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_rows_loaded": len(self.market_data),
            "total_symbols": len(self.symbol_snapshot),
            "pipeline_status": "INSTITUTIONAL_PIPELINE_ACTIVE"
        }

    # ------------------------------
    # MAIN EXECUTION FLOW
    # ------------------------------
    def execute(self):

        if self.state != ExecutionState.VALIDATED:
            raise RuntimeError("System not validated")

        self.state = ExecutionState.RUNNING

        self.safe_execute(self.load_market_data, "Load Market Data")
        self.safe_execute(self.run_intelligence_layer, "Run Intelligence Layer")

        output = self.safe_execute(
            self.build_structured_output,
            "Build Structured Output"
        )

        self.state = ExecutionState.COMPLETED
        self.pipeline_log.append("Pipeline Completed Successfully")

        return output


if __name__ == "__main__":
    brain = MasterBrain()
    brain.validate_environment()
    result = brain.execute()
    print(result)
