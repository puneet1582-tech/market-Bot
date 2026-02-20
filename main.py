# ================================
# ULTIMATE BRAIN — MAIN ENGINE
# Phase-1 Operational Intelligence System
# ================================

from flask import Flask
import threading
import time

import brain_engine
from opportunity_engine import calculate_opportunity
from risk_weighted_ranking_engine import risk_weighted_rank
from sector_intelligence_engine import sector_strength
from decision_memory_engine import save_decision
from performance_tracker_engine import log_performance
from performance_evaluation_engine import evaluate_performance
from return_estimation_engine import estimate_returns
from dashboard_output_engine import build_dashboard
from daily_report_engine import generate_daily_report
from final_report_formatter_engine import format_final_report
from sector_universe_mapper import map_sector_universe
from sector_rotation_engine import update_sector_rotation
from sector_leadership_engine import detect_sector_leaders
from capital_flow_engine import detect_capital_flow
from nse_universe_loader import load_nse_universe
from scanner_batch_engine import create_batches
from scanner_load_balancer import batch_pause
from cycle_optimizer_engine import optimized_cycle_interval
from opportunity_watchlist_engine import update_watchlist
from opportunity_persistence_engine import detect_persistent_opportunities
from conviction_score_engine import calculate_conviction_scores
from portfolio_allocation_engine import generate_portfolio_allocation
from portfolio_risk_balancer_engine import balance_portfolio
from portfolio_lifecycle_engine import track_portfolio
from portfolio_attribution_engine import calculate_portfolio_attribution
from allocation_learning_engine import allocation_learning_adjustment
from strategy_memory_engine import store_strategy_memory
from market_regime_engine import estimate_market_regime
from strategy_regime_switch_engine import adjust_strategy_bias
from signal_confidence_engine import calculate_signal_confidence
from decision_summary_engine import generate_decision_summary

from engines.telegram_alert_engine import send_telegram_alert
from engines.opportunity_trigger_engine import process_opportunity
from engines.market_mode_engine import MarketModeEngine

app = Flask(__name__)


def run_engine():
    engine = brain_engine.BrainEngine()
    market_mode_engine = MarketModeEngine()

    while True:
        try:
            stocks = load_nse_universe()
            sector_map = map_sector_universe(stocks)

            market_data = {
                "fii_flow": 500,
                "dii_flow": 200,
                "volatility_index": 18,
                "sentiment": 60,
                "index_returns": [0.3, 0.1, -0.2]
            }

            base_mode = market_mode_engine.detect_mode(market_data)
            regime_prob = estimate_market_regime(market_data)
            final_mode_report = adjust_strategy_bias(base_mode, regime_prob)

            opportunity_list = []
            capital_flow = detect_capital_flow()

            for batch in create_batches(stocks, batch_size=25):
                for s in batch:
                    result = engine.analyze_stock(s)

                    opportunity = calculate_opportunity(
                        s,
                        result.get("price", 0),
                        final_mode_report["mode"]
                    )
                    opportunity_list.append(opportunity)

                batch_pause(2)

            sector_scores = sector_strength(opportunity_list)
            update_sector_rotation(sector_scores)
            sector_leaders = detect_sector_leaders(opportunity_list)

            ranked = risk_weighted_rank(opportunity_list)
            update_watchlist(ranked[:10])
            persistent = detect_persistent_opportunities()

            conviction_ranked = calculate_conviction_scores(
                ranked,
                sector_scores,
                capital_flow,
                persistent
            )

            conviction_ranked = calculate_signal_confidence(
                conviction_ranked,
                persistent,
                regime_prob
            )

            allocation = generate_portfolio_allocation(conviction_ranked)
            balanced_allocation = balance_portfolio(allocation, sector_map)

            attribution = calculate_portfolio_attribution()

            adaptive_allocation = allocation_learning_adjustment(
                balanced_allocation,
                attribution
            )

            track_portfolio(adaptive_allocation)
            store_strategy_memory(final_mode_report["mode"], adaptive_allocation)

            decision_summary = generate_decision_summary(conviction_ranked, adaptive_allocation)

            save_decision(conviction_ranked[:10])

            for op in conviction_ranked[:5]:
                process_opportunity(op["symbol"], op, final_mode_report["mode"])
                log_performance(op["symbol"], op["mode"], op["price"])

            perf_summary = evaluate_performance()
            return_summary = estimate_returns()

            dashboard = build_dashboard(
                final_mode_report,
                sector_scores,
                conviction_ranked,
                perf_summary,
                return_summary
            )

            dashboard["sector_leaders"] = sector_leaders
            dashboard["capital_flow"] = capital_flow
            dashboard["persistent_stocks"] = persistent
            dashboard["portfolio_allocation"] = adaptive_allocation
            dashboard["portfolio_attribution"] = attribution
            dashboard["regime_probability"] = regime_prob
            dashboard["decision_summary"] = decision_summary

            # ---- Final Institutional Report ----
            formatted_report = format_final_report(dashboard)
            send_telegram_alert(formatted_report)

            print("PHASE-1 INSTITUTIONAL INTELLIGENCE SYSTEM OPERATIONAL", flush=True)

            interval = optimized_cycle_interval(len(stocks))
            time.sleep(interval)

        except Exception as e:
            print("ENGINE ERROR:", e, flush=True)
            send_telegram_alert(f"ENGINE ERROR: {e}")
            time.sleep(60)


@app.route("/")
def home():
    return "Ultimate Brain Running"


# DISABLED ENTRY POINT
# # DISABLED ENTRY POINT
    ingestion_thread = threading.Thread(target=run_engine)
    ingestion_thread.daemon = True
    ingestion_thread.start()

    try:
        send_telegram_alert("MARKET BOT STARTED — PHASE-1 OPERATIONAL")
    except Exception as e:
        print("Telegram startup alert failed:", e)

    app.run(host="0.0.0.0", port=10000)

# ===============================
# PHASE-2 FINAL ACTIVATION LAYER
# ===============================
try:
    from phase2_pipeline_integration import apply_phase2_intelligence

    dashboard = apply_phase2_intelligence(
        dashboard,
        conviction_ranked,
        regime_prob.get("score", 50),
        sector_scores,
        market_data.get("volatility_index", 20)
    )
except Exception as _phase2_err:
    print("PHASE-2 ACTIVATION ERROR:", _phase2_err, flush=True)


# ===============================
# PHASE-2 CLASSIFICATION ACTIVATION
# ===============================
try:
    from phase2_classification_activation import apply_classification
    dashboard = apply_classification(dashboard)
except Exception as _class_err:
    print("PHASE-2 CLASSIFICATION ERROR:", _class_err, flush=True)


# ===============================
# PHASE-3 ADAPTIVE + MEMORY ACTIVATION
# ===============================
try:
    from phase3_adaptive_activation import apply_adaptive_learning
    from phase3_memory_activation import apply_memory_layer

    dashboard = apply_adaptive_learning(dashboard)
    dashboard = apply_memory_layer(dashboard)

except Exception as _phase3_err:
    print("PHASE-3 ACTIVATION ERROR:", _phase3_err, flush=True)


# ===============================
# PHASE-3 PORTFOLIO OPTIMIZATION ACTIVATION
# ===============================
try:
    from phase3_portfolio_optimization_activation import apply_portfolio_optimization
    dashboard = apply_portfolio_optimization(dashboard)
except Exception as _opt_err:
    print("PHASE-3 PORTFOLIO OPT ERROR:", _opt_err, flush=True)


# ===============================
# PHASE-4 REPORTING ACTIVATION
# ===============================
try:
    from phase4_reporting_activation import apply_reporting_layer
    dashboard = apply_reporting_layer(dashboard)
except Exception as _report_err:
    print("PHASE-4 REPORTING ERROR:", _report_err, flush=True)


# ===============================
# PHASE-4 DISPATCH ACTIVATION
# ===============================
try:
    from phase4_dispatch_activation import apply_dispatch_layer
    dashboard = apply_dispatch_layer(dashboard)
except Exception as _dispatch_err:
    print("PHASE-4 DISPATCH ERROR:", _dispatch_err, flush=True)


# ===============================
# PHASE-4 ARCHIVE ACTIVATION
# ===============================
try:
    from phase4_archive_activation import apply_archive_layer
    dashboard = apply_archive_layer(dashboard)
except Exception as _archive_err:
    print("PHASE-4 ARCHIVE ERROR:", _archive_err, flush=True)


# ===============================
# PHASE-5 GLOBAL MARKET LINKAGE
# ===============================
try:
    from phase5_linkage_activation import apply_global_linkage
    dashboard = apply_global_linkage(dashboard)
except Exception as _link_err:
    print("PHASE-5 LINKAGE ERROR:", _link_err, flush=True)


# ===============================
# PHASE-5 GLOBAL SIGNAL FUSION
# ===============================
try:
    from phase5_signal_fusion_activation import apply_global_signal_fusion
    dashboard = apply_global_signal_fusion(dashboard)
except Exception as _fusion_err:
    print("PHASE-5 FUSION ERROR:", _fusion_err, flush=True)


# ===============================
# PHASE-5 OPPORTUNITY MAP ACTIVATION
# ===============================
try:
    from phase5_opportunity_map_activation import apply_opportunity_map
    dashboard = apply_opportunity_map(dashboard)
except Exception as _omap_err:
    print("PHASE-5 OPPORTUNITY MAP ERROR:", _omap_err, flush=True)


# ===============================
# PHASE-6 STRATEGIC DECISION ACTIVATION
# ===============================
try:
    from phase6_strategy_activation import apply_strategy_layer
    dashboard = apply_strategy_layer(dashboard)
except Exception as _strategy_err:
    print("PHASE-6 STRATEGY ERROR:", _strategy_err, flush=True)


# ===============================
# PHASE-6 MULTI-CYCLE ALLOCATION ACTIVATION
# ===============================
try:
    from phase6_multicycle_allocation_activation import apply_multicycle_allocation
    dashboard = apply_multicycle_allocation(dashboard)
except Exception as _mca_err:
    print("PHASE-6 MULTICYCLE ALLOCATION ERROR:", _mca_err, flush=True)


# ===============================
# PHASE-7 RISK GOVERNANCE ACTIVATION
# ===============================
try:
    from phase7_risk_governance_activation import apply_risk_governance
    dashboard = apply_risk_governance(dashboard)
except Exception as _risk_err:
    print("PHASE-7 RISK GOVERNANCE ERROR:", _risk_err, flush=True)


# ===============================
# PHASE-7 CRISIS CAPITAL SHIELD
# ===============================
try:
    from phase7_crisis_shield_activation import apply_crisis_shield
    dashboard = apply_crisis_shield(dashboard)
except Exception as _shield_err:
    print("PHASE-7 CRISIS SHIELD ERROR:", _shield_err, flush=True)


# ===============================
# PHASE-8 STRATEGY EVOLUTION
# ===============================
try:
    from phase8_strategy_evolution_activation import apply_strategy_evolution
    dashboard = apply_strategy_evolution(dashboard)
except Exception as _evo_err:
    print("PHASE-8 STRATEGY EVOLUTION ERROR:", _evo_err, flush=True)


# ===============================
# PHASE-8 WEIGHT CALIBRATION
# ===============================
try:
    from phase8_weight_calibration_activation import apply_weight_calibration
    dashboard = apply_weight_calibration(dashboard)
except Exception as _cal_err:
    print("PHASE-8 WEIGHT CALIBRATION ERROR:", _cal_err, flush=True)


# ===============================
# PHASE-9 META INTELLIGENCE FEEDBACK
# ===============================
try:
    from phase9_meta_feedback_activation import apply_meta_feedback
    dashboard = apply_meta_feedback(dashboard)
except Exception as _meta_err:
    print("PHASE-9 META FEEDBACK ERROR:", _meta_err, flush=True)


# ===============================
# PHASE-9 SELF IMPROVEMENT ACTIVATION
# ===============================
try:
    from phase9_self_improvement_activation import apply_self_improvement
    dashboard = apply_self_improvement(dashboard)
except Exception as _si_err:
    print("PHASE-9 SELF IMPROVEMENT ERROR:", _si_err, flush=True)


# ===============================
# PHASE-10 MARKET MODE CONTROLLER
# ===============================
try:
    from phase10_market_mode_activation import apply_market_mode_controller
    dashboard = apply_market_mode_controller(dashboard)
except Exception as _mm_err:
    print("PHASE-10 MARKET MODE ERROR:", _mm_err, flush=True)


# ===============================
# PHASE-10 CAPITAL DEPLOYMENT ACTIVATION
# ===============================
try:
    from phase10_capital_deployment_activation import apply_capital_deployment
    dashboard = apply_capital_deployment(dashboard)
except Exception as _cd_err:
    print("PHASE-10 CAPITAL DEPLOYMENT ERROR:", _cd_err, flush=True)


# ===============================
# PHASE-11 MASTER BRAIN CONTROLLER
# ===============================
try:
    from phase11_master_controller_activation import apply_master_controller
    dashboard = apply_master_controller(dashboard)
except Exception as _mb_err:
    print("PHASE-11 MASTER CONTROLLER ERROR:", _mb_err, flush=True)

