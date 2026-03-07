import importlib

ENGINES = [

    "core.nse_bhavcopy_engine",
    "core.nse_universe_engine",
    "core.fundamental_ingestion_engine",
    "core.fundamental_10y_engine",
    "core.fii_dii_trend_engine",
    "core.business_evolution_engine",
    "core.global_impact_engine",
    "core.news_signal_engine",
    "core.mode_engine",
    "core.opportunity_detection_engine"

]


def run_engine(module_name):

    try:

        module = importlib.import_module(module_name)

        if hasattr(module, "run"):
            print(f"Running {module_name}")
            module.run()
        else:
            print(f"Skipped {module_name} (no run function)")

    except Exception as e:

        print(f"Engine failed: {module_name} -> {e}")


def main():

    print("\nULTIMATE BRAIN MASTER CONTROLLER\n")

    for engine in ENGINES:

        run_engine(engine)

    print("\nSYSTEM EXECUTION COMPLETE\n")


if __name__ == "__main__":
    main()

