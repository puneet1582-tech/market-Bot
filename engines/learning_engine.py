import pandas as pd
import os

DATA_PATH = "data/learning_log.csv"

class LearningEngine:
    def __init__(self):
        if not os.path.exists(DATA_PATH):
            df = pd.DataFrame(columns=["symbol", "decision", "result"])
            df.to_csv(DATA_PATH, index=False)
        self.df = pd.read_csv(DATA_PATH)

    def log_result(self, symbol, decision, result):
        new_row = {
            "symbol": symbol,
            "decision": decision,
            "result": result
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.df.to_csv(DATA_PATH, index=False)

    def accuracy(self):
        if self.df.empty:
            return "NO DATA YET"

        correct = len(self.df[self.df["decision"] == self.df["result"]])
        total = len(self.df)

        return round((correct / total) * 100, 2)
