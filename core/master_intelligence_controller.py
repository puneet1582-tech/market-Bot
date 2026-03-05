from real_fundamental_engine import build_fundamental_core
from business_evolution_engine import build_business_evolution
from fii_dii_trend_engine import build_institutional_trend
from sector_money_flow_engine import build_sector_strength
from multibagger_detection_engine import detect_multibaggers


def run_full_intelligence():

    print("\nULTIMATE BRAIN — MASTER INTELLIGENCE PIPELINE\n")

    print("RUNNING: Fundamental Engine")
    build_fundamental_core()

    print("\nRUNNING: Business Evolution Engine")
    build_business_evolution()

    print("\nRUNNING: FII/DII Trend Engine")
    build_institutional_trend()

    print("\nRUNNING: Sector Money Flow Engine")
    build_sector_strength()

    print("\nRUNNING: Multibagger Detection Engine")
    detect_multibaggers()

    print("\nPIPELINE COMPLETE\n")
