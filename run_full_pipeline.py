import subprocess
import sys

def run_step(name, cmd):

    print("\n==============================")
    print("RUNNING:", name)
    print("==============================")

    result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        print("FAILED:", name)
        sys.exit(1)

    print("SUCCESS:", name)


def main():

    run_step(
        "NSE Downloader",
        "python engines/data_core/adaptive_nse_downloader.py"
    )

    run_step(
        "Market Price Engine",
        "python engines/data_core/market_price_engine.py"
    )

    run_step(
        "Momentum Engine",
        "python engines/market/momentum_engine.py"
    )

    run_step(
        "Sector Money Flow",
        "python engines/market/sector_money_flow_engine.py"
    )

    run_step(
        "Market Mode",
        "python engines/market/market_mode_engine.py"
    )

    run_step(
        "Company Intelligence",
        "python run_company_intelligence.py"
    )

    run_step(
        "Ownership Intelligence",
        "python engines/market/ownership_intelligence_engine.py"
    )

    run_step(
        "Master Brain",
        "python run_master_brain.py"
    )

    print("\nPIPELINE COMPLETE")


if __name__ == "__main__":
    main()
