def calculate_final_score(fundamental, technical, risk, valuation):

    final_score = (
        fundamental["score"] +
        technical["score"] +
        risk["score"] +
        valuation["score"]
    )

    if final_score >= 75:
        recommendation = "🟢 STRONG BUY"

    elif final_score >= 60:
        recommendation = "🟡 BUY"

    elif final_score >= 45:
        recommendation = "🟠 HOLD"

    else:
        recommendation = "🔴 SELL"

    return {
        "final_score": final_score,
        "recommendation": recommendation,
    }