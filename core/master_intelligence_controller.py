from core.fundamental_ingestion_engine import build_fundamental_dataset
from core.nse_price_engine import build_price_dataset
from core.nse_universe_engine import build_nse_universe
from core.opportunity_detection_engine import detect_opportunities
import sys
import os

# ensure project root path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from core.real_fundamental_engine import build_fundamental_core
from core.business_evolution_engine import build_business_evolution
from core.fii_dii_trend_engine import build_institutional_trend
from core.sector_money_flow_engine import build_sector_strength
from core.multibagger_detection_engine import detect_multibaggers


def run_full_intelligence():

    print("\nULTIMATE BRAIN — MASTER INTELLIGENCE PIPELINE\n")
    print("RUNNING: NSE Universe Engine")
    print("RUNNING: NSE Price Engine")
    print("RUNNING: Fundamental Ingestion Engine")
    build_fundamental_dataset()

    build_price_dataset()

    build_nse_universe()


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

    print("\nRUNNING: Opportunity Detection Engine")
    detect_opportunities()

    print("\nPIPELINE COMPLETE\n")

