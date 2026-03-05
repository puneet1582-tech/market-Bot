import os
import subprocess

ENGINES = [
    "core/real_fundamental_engine.py",
    "core/business_evolution_engine.py",
    "core/fii_dii_trend_engine.py",
    "core/sector_money_flow_engine.py",
    "core/multibagger_detection_engine.py"
]

def run_engine(engine):

    if not os.path.exists(engine):
        print("Missing:", engine)
        return

    print("\nRUNNING:", engine)
    subprocess.run(["python3", engine])


def run_full_intelligence():

    print("\nULTIMATE BRAIN — MASTER INTELLIGENCE PIPELINE\n")

    for engine in ENGINES:
        run_engine(engine)

    print("\nPIPELINE COMPLETE\n")


# disabled_entry_point
    run_full_intelligence()
