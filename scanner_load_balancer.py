# SCANNER LOAD BALANCER
# Controls batch processing pacing for stability

import time

def batch_pause(delay=2):
    try:
        time.sleep(delay)
    except:
        pass
