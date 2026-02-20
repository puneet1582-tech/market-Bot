"""
ULTIMATE BRAIN
INSTITUTIONAL MASTER ORCHESTRATOR
PHASE-A HARDENED CORE
"""

import sys
import traceback
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class ExecutionState:
    INITIALIZED = "INITIALIZED"
    VALIDATED = "VALIDATED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class MasterBrain:

    def __init__(self):
        self.state = ExecutionState.INITIALIZED
        self.start_time = datetime.utcnow()
        self.pipeline_log = []

    # ------------------------------
    # SYSTEM VALIDATION GATE
    # ------------------------------
    def validate_environment(self):
        required_files = ["run.py", "brain_control.py"]
        for file in required_files:
            if not (PROJECT_ROOT / file).exists():
                raise RuntimeError(f"CRITICAL: Missing required file -> {file}")

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
            error_msg = f"FAILED: {name} | {str(e)}"
            self.pipeline_log.append(error_msg)
            traceback.print_exc()
            raise RuntimeError(error_msg)

    # ------------------------------
    # PIPELINE PLACEHOLDER (ENGINE HOOKS)
    # ------------------------------
    def load_market_data(self):
        # Real integration will connect Step-2 ingestion engine
        return "Market Data Loaded"

    def run_intelligence_layer(self):
        # Will later connect fundamentals + sector + news engines
        return "Intelligence Layer Executed"

    def build_structured_output(self):
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "mode": "INSTITUTIONAL_PIPELINE_ACTIVE",
            "status": "PIPELINE_OK"
        }

    # ------------------------------
    # MAIN EXECUTION FLOW
    # ------------------------------
    def execute(self):
        if self.state != ExecutionState.VALIDATED:
            raise RuntimeError("System not validated before execution")

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


# -------------------------------------------------
# ENTRY LOCK (NO EXTRA __main__ ALLOWED ANYWHERE)
# -------------------------------------------------
if __name__ == "__main__":
    brain = MasterBrain()
    brain.validate_environment()
    result = brain.execute()

    print("\n=========== MASTER BRAIN EXECUTION ===========")
    print(result)
    print("==============================================")
