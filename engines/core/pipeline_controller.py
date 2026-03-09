import time
import traceback
import pandas as pd
import os


from engines.market.company_intelligence_engine import run as run_company
from engines.market.ownership_intelligence_engine import run as run_ownership
from engines.market.sector_intelligence_engine import run as run_sector
from engines.macro.global_macro_engine import run as run_macro
from engines.signals.signal_fusion_engine import run as run_signals
from engines.alpha.alpha_discovery_engine import run as run_alpha
from engines.opportunity.opportunity_intelligence_engine import run as run_opportunity
from engines.master.master_brain_engine import run as run_master


RUN_LOG = "data/system_runs/run_history.csv"


def record_run(step,status,duration,error=""):

    row = {
        "timestamp":pd.Timestamp.now(),
        "step":step,
        "status":status,
        "duration":duration,
        "error":error
    }

    if os.path.exists(RUN_LOG):

        df = pd.read_csv(RUN_LOG)
        df = pd.concat([df,pd.DataFrame([row])])

    else:

        df = pd.DataFrame([row])

    df.to_csv(RUN_LOG,index=False)



def execute_step(name,func):

    start = time.time()

    try:

        print("RUNNING:",name)

        func()

        duration = round(time.time()-start,2)

        record_run(name,"SUCCESS",duration)

        print("SUCCESS:",name)

    except Exception as e:

        duration = round(time.time()-start,2)

        record_run(name,"FAILED",duration,str(e))

        print("FAILED:",name)

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
        ("Master Brain",run_master)

    ]

    start = time.time()

    for name,func in steps:

        execute_step(name,func)

    total = round(time.time()-start,2)

    print("PIPELINE COMPLETE")
    print("TOTAL TIME:",total,"seconds")



if __name__ == "__main__":

    run_pipeline()
