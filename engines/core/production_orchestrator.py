import time
import logging
import traceback

from engines.market.company_intelligence_engine import run as run_company
from engines.market.ownership_intelligence_engine import run as run_ownership
from engines.market.sector_intelligence_engine import run as run_sector
from engines.market.market_mode_engine import run as run_market
from engines.master.master_brain_engine import run as run_master


logging.basicConfig(
    filename="logs/system_run.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


class PipelineStep:

    def __init__(self, name, func):
        self.name = name
        self.func = func

    def execute(self):

        start = time.time()

        logging.info(f"START {self.name}")

        try:
            self.func()

            duration = round(time.time() - start,2)

            logging.info(f"SUCCESS {self.name} ({duration}s)")

        except Exception as e:

            logging.error(f"FAILED {self.name}")
            logging.error(traceback.format_exc())

            raise e


class MasterPipeline:

    def __init__(self):

        self.steps = [

            PipelineStep(
                "Company Intelligence Engine",
                run_company
            ),

            PipelineStep(
                "Ownership Intelligence Engine",
                run_ownership
            ),

            PipelineStep(
                "Sector Intelligence Engine",
                run_sector
            ),

            PipelineStep(
                "Market Mode Engine",
                run_market
            ),

            PipelineStep(
                "Master Brain Engine",
                run_master
            )

        ]

    def run(self):

        logging.info("PIPELINE START")

        start = time.time()

        for step in self.steps:
            step.execute()

        total = round(time.time() - start,2)

        logging.info(f"PIPELINE COMPLETE ({total}s)")
        print("SYSTEM PIPELINE COMPLETE")


def run():

    pipeline = MasterPipeline()

    pipeline.run()


if __name__ == "__main__":
    run()
