import time
import traceback
import pandas as pd
import os


from run_company_intelligence import run as run_company
from run_ownership_intelligence import run as run_ownership
from run_sector_intelligence import run as run_sector
from run_global_macro import run as run_macro
from run_signal_fusion import run as run_signals
from run_alpha_engine import run as run_alpha
from run_opportunity_engine import run as run_opportunity
from run_master_brain import run as run_master


RUN_LOG = "data/system_runs/run_history.csv"


def record_run(step,status,duration,error=""):

    row = {
        "timestamp":pd.Timestamp.now(),
        "step":step,
        "status":status,
        "duration_sec":duration,
        "error":error
    }

    df = pd.DataFrame([row])

    if os.path.exists(RUN_LOG):

        prev = pd.read_csv(RUN_LOG)

        df = pd.concat([prev,df],ignore_index=True)

    df.to_csv(RUN_LOG,index=False)


def execute_step(name,func):

    start = time.time()

    try:

        func()

        duration = round(time.time()-start,2)

        record_run(name,"SUCCESS",duration)

        print(f"{name} completed in {duration}s")

    except Exception as e:

        duration = round(time.time()-start,2)

        record_run(name,"FAILED",duration,str(e))

        print(f"{name} failed")

        print(traceback.format_exc())

        raise e



def run_pipeline():

    steps = [

        ("Company Intelligence",run_company),

        ("Ownership Intelligence",run_ownership),

        ("Sector Intelligence",run_sector),

        ("Global Macro Intelligence",run_macro),

        ("Signal Fusion",run_signals),

        ("Alpha Discovery",run_alpha),

        ("Opportunity Intelligence",run_opportunity),

        ("Master Brain Decision",run_master)

    ]

    print("Starting Institutional Pipeline")

    for name,func in steps:

        execute_step(name,func)

    print("Pipeline execution complete")


if __name__ == "__main__":

    run_pipeline()
