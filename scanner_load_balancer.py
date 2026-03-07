# SCANNER LOAD BALANCER
# Controls batch processing pacing for stability

import time

def batch_pause(delay=2):
    try:
        time.sleep(delay)
    except:
        pass


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
