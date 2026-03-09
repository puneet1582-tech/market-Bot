import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.master_brain_engine import MasterBrainEngine
import json

class MasterIntelligenceController:

    def __init__(self):
        self.brain = MasterBrainEngine()

    def run(self):

        print("MASTER INTELLIGENCE CONTROLLER STARTED")

        report = self.brain.run()

        try:
            with open("data/master_brain_report.json","w") as f:
                json.dump(report,f,indent=2)
        except:
            pass

        print("MASTER INTELLIGENCE REPORT GENERATED")

        return report


def run():

    controller = MasterIntelligenceController()

    return controller.run()


if __name__ == "__main__":
    run()
