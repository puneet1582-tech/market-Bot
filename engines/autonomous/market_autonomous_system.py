import os
import time
import logging
from datetime import datetime

from engines.core.production_orchestrator import run as run_pipeline


STATE_FILE = "runtime/state/system_state.txt"
LOG_FILE = "runtime/logs/autonomous.log"


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


class MarketClock:

    MARKET_START = (9, 5)
    MARKET_END = (15, 45)

    @staticmethod
    def now():
        return datetime.now()

    @staticmethod
    def is_market_time():

        now = datetime.now()

        start = now.replace(
            hour=MarketClock.MARKET_START[0],
            minute=MarketClock.MARKET_START[1],
            second=0
        )

        end = now.replace(
            hour=MarketClock.MARKET_END[0],
            minute=MarketClock.MARKET_END[1],
            second=0
        )

        return start <= now <= end


class SystemState:

    @staticmethod
    def write(state):

        with open(STATE_FILE, "w") as f:
            f.write(state)

    @staticmethod
    def read():

        if not os.path.exists(STATE_FILE):
            return "IDLE"

        with open(STATE_FILE) as f:
            return f.read().strip()


class AutonomousMarketSystem:

    def __init__(self):

        self.last_run = None

    def should_run_pipeline(self):

        if not MarketClock.is_market_time():
            return False

        now = datetime.now()

        if self.last_run is None:
            return True

        minutes = (now - self.last_run).seconds / 60

        return minutes >= 60

    def run_pipeline(self):

        logging.info("PIPELINE START")

        SystemState.write("RUNNING")

        try:

            run_pipeline()

            logging.info("PIPELINE COMPLETE")

        except Exception as e:

            logging.error("PIPELINE FAILED")
            logging.error(str(e))

        SystemState.write("IDLE")

        self.last_run = datetime.now()

    def loop(self):

        logging.info("AUTONOMOUS SYSTEM STARTED")

        while True:

            try:

                if self.should_run_pipeline():

                    self.run_pipeline()

                time.sleep(60)

            except Exception as e:

                logging.error("SYSTEM LOOP ERROR")
                logging.error(str(e))

                time.sleep(60)


def run():

    system = AutonomousMarketSystem()

    system.loop()


if __name__ == "__main__":
    run()
