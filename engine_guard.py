import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

if ROOT not in sys.path:
    sys.path.append(ROOT)

CORE = os.path.join(ROOT, "core")
ENG = os.path.join(ROOT, "engines")

if CORE not in sys.path:
    sys.path.append(CORE)

if ENG not in sys.path:
    sys.path.append(ENG)

print("ENGINE PATHS INITIALIZED")
