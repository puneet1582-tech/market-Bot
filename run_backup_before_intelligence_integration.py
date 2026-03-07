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


# disabled_entry_point
    output = main()
    print(output)


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
