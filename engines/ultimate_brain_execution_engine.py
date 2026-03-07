import sys
import os
import importlib
import inspect

sys.path.append(os.getcwd())


class UltimateBrainExecutionEngine:

    def run_engine(self, module_name):

        try:

            module = importlib.import_module(module_name)

            functions = inspect.getmembers(module, inspect.isfunction)

            if not functions:
                print(f"[SKIP] No executable function in {module_name}")
                return

            func_name, func = functions[0]

            print(f"[RUN] {module_name}.{func_name}()")

            func()

        except Exception as e:

            print(f"[ERROR] {module_name} -> {e}")


    def run(self):

        print("\n===== ULTIMATE BRAIN EXECUTION STARTED =====\n")

        engines = [

            "engines.nse_universe_master_builder",
            "engines.price_ingestion_production_engine",
            "engines.fundamentals_master_ingestion_engine",
            "engines.institutional_ownership_engine",
            "engines.global_news_engine",
            "engines.sector_money_flow_engine",
            "engines.daily_top20_opportunity_engine",
            "engines.telegram_top20_delivery_engine"

        ]

        for engine in engines:

            self.run_engine(engine)

        print("\n===== ULTIMATE BRAIN EXECUTION COMPLETE =====\n")


if __name__ == "__main__":

    brain = UltimateBrainExecutionEngine()

    brain.run()
