"""
ULTIMATE BRAIN
PRIMARY ENTRY POINT
INSTITUTIONAL SINGLE EXECUTION MODEL
"""

from core.master_brain import MasterBrain


def main():
    brain = MasterBrain()
    brain.validate_environment()
    result = brain.execute()
    return result


if __name__ == "__main__":
    output = main()
    print(output)
