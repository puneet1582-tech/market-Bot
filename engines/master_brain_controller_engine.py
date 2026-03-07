import logging
logging.basicConfig(level=logging.INFO)

class MasterBrainController:
    def run(self):
        logging.info("MASTER BRAIN CONTROLLER RUNNING")

def run_master_brain_controller():
    controller = MasterBrainController()
    controller.run()


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
