class MultibaggerEngine:

    def evaluate(self, business, institutional, sector, macro, impact):
        """
        Inputs are already computed layer outputs.
        No scoring model.
        Structured layered interpretation only.
        """

        flags = {
            "structural_compounder": False,
            "institutional_alignment": False,
            "sector_tailwind": False,
            "macro_resilience": False,
            "low_event_risk": False
        }

        # 1️⃣ Structural business strength
        if business.get("structural_interpretation") == "High Probability Structural Compounder":
            flags["structural_compounder"] = True

        # 2️⃣ Institutional conviction
        if (
            institutional.get("promoter_trend") == "Accumulating" and
            institutional.get("fii_trend") == "Accumulating"
        ):
            flags["institutional_alignment"] = True

        # 3️⃣ Sector tailwind
        if sector.get("cyclical_status") == "Structural Growth":
            flags["sector_tailwind"] = True

        # 4️⃣ Macro resilience
        if macro.get("interest_rate_impact") in ["Stable", "Falling"]:
            flags["macro_resilience"] = True

        # 5️⃣ Event sensitivity
        if impact:
            if impact.get("risk_category") == "Low Sensitivity":
                flags["low_event_risk"] = True
        else:
            flags["low_event_risk"] = True  # No major event applied

        final_view = self._final_classification(flags)

        return {
            "multibagger_flags": flags,
            "final_multibagger_view": final_view
        }

    def _final_classification(self, flags):
        if all(flags.values()):
            return "High Conviction Multibagger Candidate"
        elif flags["structural_compounder"] and flags["institutional_alignment"]:
            return "Emerging Multibagger - Monitor Closely"
        elif not flags["structural_compounder"]:
            return "Not a Structural Multibagger"
        else:
            return "Partial Alignment - Needs Deeper Review"


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
