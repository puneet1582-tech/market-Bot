def exit_engine(row, decision, tech, nf, score):
    """
    Hybrid Exit Engine:
    Long-term + Swing logic
    """

    # FULL EXIT conditions
    if score < 40 or tech == "WEAK" or nf == "NEGATIVE":
        return "EXIT FULL"

    # PARTIAL EXIT (protect profit)
    if tech == "WAIT" and decision.startswith("BUY"):
        return "PARTIAL EXIT (50%)"

    # HOLD / ADD
    if decision.startswith("BUY"):
        return "HOLD / ADD ON DIPS"

    # SPECULATIVE handling
    if "SPECULATIVE" in decision:
        return "TIGHT STOPLOSS / QUICK EXIT"

    return "HOLD"

