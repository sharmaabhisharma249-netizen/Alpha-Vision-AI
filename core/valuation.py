def calculate_valuation_score(fundamental):

    score = 20

    pe = fundamental.get("pe")
    pb = fundamental.get("pb")

    # P/E Score
    if pe is not None:
        if pe <= 20:
            score += 5
        elif pe <= 30:
            score += 3
        elif pe > 50:
            score -= 4

    # P/B Score
    if pb is not None:
        if pb <= 3:
            score += 5
        elif pb > 8:
            score -= 4

    score = max(score, 0)

    if score >= 25:
        valuation = "🟢 Undervalued"
    elif score >= 20:
        valuation = "🟡 Fairly Valued"
    else:
        valuation = "🔴 Overvalued"

    return {
        "score": score,
        "valuation": valuation,
        "pe": pe,
        "pb": pb,
    }