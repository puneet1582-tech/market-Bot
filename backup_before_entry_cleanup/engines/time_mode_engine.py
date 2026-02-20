import csv
import datetime

class TimeModeEngine:
    def __init__(self, filepath="data/time_mode.csv"):
        self.filepath = filepath

    def get_allowed_mode(self):
        with open(self.filepath, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                return row["mode"]
        return "DEFENSIVE"

    def is_trade_time(self, market_mode):
        # 1. Check time window (9:30 to 14:30)
        now = datetime.datetime.now().time()
        start = datetime.time(9, 30)
        end = datetime.time(14, 30)

        if not (start <= now <= end):
            return False, "Outside trading time"

        # 2. Check allowed mode from CSV
        allowed_mode = self.get_allowed_mode()

        if allowed_mode != market_mode:
            return False, f"TimeMode blocks trading (allowed: {allowed_mode})"

        return True, "Time allows trading"
