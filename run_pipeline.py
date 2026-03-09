import subprocess
import sys

def run_step(script):
    print(f"\nRunning: {script}")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"Error running {script}")
        sys.exit(1)

def main():

    steps = [
        "engines/market/bhavcopy_parser.py",
        "engines/market/liquidity_filter.py",
        "engines/market/momentum_engine.py",
        "engines/market/opportunity_engine.py"
    ]

    for step in steps:
        run_step(step)

    print("\nPipeline completed successfully")

if __name__ == "__main__":
    main()
