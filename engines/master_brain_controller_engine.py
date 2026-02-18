import logging
logging.basicConfig(level=logging.INFO)

class MasterBrainController:
    def run(self):
        logging.info("MASTER BRAIN CONTROLLER RUNNING")

def run_master_brain_controller():
    controller = MasterBrainController()
    controller.run()
