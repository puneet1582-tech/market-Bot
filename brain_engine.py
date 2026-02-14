import sqlite3
import datetime
import time
from threading import Thread

DB_NAME = "ultimate_brain_data.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS system_log(
        message TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized")


def ingestion_loop():
    while True:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO system_log VALUES (?, ?)",
            ("Step-2 ingestion running", str(datetime.datetime.now()))
        )
        conn.commit()
        conn.close()
        print("Step-2 ingestion running...")
        time.sleep(3600)


def start_step2_engine():
    init_database()
    Thread(target=ingestion_loop, daemon=True).start()
    print("STEP-2 ENGINE ACTIVE")
