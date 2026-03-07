# SCHEDULE CONTROLLER ENGINE
# Controls execution frequency based on market hours

from datetime import datetime

def get_cycle_interval():
    now = datetime.now()

    # NSE Market hours approx 9:15 to 15:30
    if now.hour > 9 and now.hour < 15:
        return 300      # 5 minutes during market hours
    else:
        return 1800     # 30 minutes during off-market


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
