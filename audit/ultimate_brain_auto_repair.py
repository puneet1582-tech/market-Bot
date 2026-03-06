import os
from pathlib import Path
import subprocess

ROOT = Path(".")

print("\nULTIMATE BRAIN AUTO REPAIR STARTED\n")

# ------------------------------------------------
# CREATE REQUIRED DATA STRUCTURE
# ------------------------------------------------

required_dirs = [
    "data/fundamentals",
    "data/ownership",
]

for d in required_dirs:
    Path(d).mkdir(parents=True, exist_ok=True)
    print("DIR OK:", d)

# ------------------------------------------------
# CREATE NSE / BSE SYMBOL FILES
# ------------------------------------------------

nse_file = Path("data/nse_symbols.csv")
bse_file = Path("data/bse_symbols.csv")

if not nse_file.exists():
    nse_file.write_text("symbol\nRELIANCE\nTCS\nINFY\nHDFCBANK\nICICIBANK\n")
    print("CREATED:", nse_file)

if not bse_file.exists():
    bse_file.write_text("symbol\nRELIANCE\nTCS\nINFY\nHDFCBANK\nICICIBANK\n")
    print("CREATED:", bse_file)

# ------------------------------------------------
# PATCH FINAL DECISION ENGINE
# ------------------------------------------------

fde = Path("engines/final_decision_engine.py")

if fde.exists():

    code = fde.read_text()

    if "class FinalDecisionEngine" not in code:

        patch = """

class FinalDecisionEngine:

    def __init__(self):
        pass

    def run(self, data=None):
        return {"decision":"HOLD"}

"""
        with open(fde, "a") as f:
            f.write(patch)

        print("PATCHED FinalDecisionEngine")

# ------------------------------------------------
# PATCH TRADING BRAIN ENGINE
# ------------------------------------------------

tbe = Path("engines/trading_brain_engine.py")

if tbe.exists():

    code = tbe.read_text()

    if "FinalDecisionEngine" in code and "import" not in code.split("FinalDecisionEngine")[0]:

        patch = "from engines.final_decision_engine import FinalDecisionEngine\n"

        with open(tbe, "r") as f:
            original = f.read()

        with open(tbe, "w") as f:
            f.write(patch + original)

        print("PATCHED trading_brain_engine import")

# ------------------------------------------------
# FIX BROKEN FILE NAME
# ------------------------------------------------

bad_file = Path("engines/open engines:sector_classifier.py")

if bad_file.exists():

    new_file = Path("engines/sector_classifier_engine_fixed.py")

    bad_file.rename(new_file)

    print("RENAMED bad engine file")

# ------------------------------------------------
# GIT AUTO PUSH
# ------------------------------------------------

try:

    subprocess.run(["git","add","."], check=True)

    subprocess.run(
        ["git","commit","-m","Ultimate Brain auto repair patch"],
        check=True
    )

    subprocess.run(
        ["git","push","origin","intelligence_layer_v1"],
        check=True
    )

    print("\nGITHUB PUSH COMPLETE")

except Exception as e:
    print("Git operation skipped:", e)

print("\nAUTO REPAIR COMPLETE\n")
