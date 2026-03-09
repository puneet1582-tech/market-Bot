import time


from engines.signals.signal_fusion_engine import run as run_signals
from engines.alpha.alpha_discovery_engine import run as run_alpha
from engines.opportunity.opportunity_intelligence_engine import run as run_opportunity
from engines.portfolio.portfolio_construction_engine import run as run_portfolio


def step(name,func):

    print("")
    print("RUNNING:",name)

    start = time.time()

    func()

    end = time.time()

    print("COMPLETED:",name,"(",round(end-start,2),"sec )")


def run():

    step(
        "Signal Fusion Engine",
        run_signals
    )

    step(
        "Alpha Discovery Engine",
        run_alpha
    )

    step(
        "Opportunity Intelligence Engine",
        run_opportunity
    )

    step(
        "Portfolio Construction Engine",
        run_portfolio
    )


if __name__ == "__main__":
    run()
