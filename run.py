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


# ===============================
# OPTIONAL REAL INTELLIGENCE LAYER
# ===============================

try:
    from real_intelligence_layer.master_intelligence_engine import MasterIntelligenceEngine

    def run_real_intelligence_layer(company_data):
        engine = MasterIntelligenceEngine()
        return engine.run_full_analysis(company_data)

except Exception as e:
    print("Real Intelligence Layer not activated:", e)

# ===============================

