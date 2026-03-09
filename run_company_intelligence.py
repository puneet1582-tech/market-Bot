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

        "engines/market/company_intelligence_engine.py"

    ]

    for step in steps:
        run_step(step)

    print("\nCompany intelligence completed")


if __name__ == "__main__":
    main()
