import pandas as pd
import os


FILES = {
    "company_intelligence":"data/processed/company_intelligence.csv",
    "ownership_intelligence":"data/processed/ownership_intelligence.csv",
    "sector_intelligence":"data/processed/sector_intelligence.csv",
    "signal_matrix":"data/processed/signal_matrix.csv",
    "alpha_opportunities":"data/processed/alpha_opportunities.csv"
}


OUTPUT = "data/system_audit/system_health_report.csv"


def inspect_file(name,path):

    if not os.path.exists(path):

        return {
            "file":name,
            "status":"MISSING",
            "rows":0,
            "columns":""
        }

    df = pd.read_csv(path)

    return {
        "file":name,
        "status":"OK",
        "rows":len(df),
        "columns":",".join(df.columns)
    }


def run():

    results = []

    for name,path in FILES.items():

        results.append(
            inspect_file(name,path)
        )

    out = pd.DataFrame(results)

    out.to_csv(
        OUTPUT,
        index=False
    )

    print("SYSTEM AUDIT COMPLETE")
    print(out)


if __name__ == "__main__":
    run()
