from core.master_brain_engine import MasterBrainEngine

class MasterIntelligenceController:

    def __init__(self):
        self.brain = MasterBrainEngine()

    def run(self):

        print("MASTER INTELLIGENCE CONTROLLER STARTED")

        report = self.brain.run()

        try:
            with open("data/master_brain_report.json","w") as f:
                import json
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
