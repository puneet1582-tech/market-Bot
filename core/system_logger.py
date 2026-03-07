import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("ultimate_brain")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/ultimate_brain.log")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def log(msg):
    logger.info(msg)


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
