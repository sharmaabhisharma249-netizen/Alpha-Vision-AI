def calculate_risk_score(fundamental_data):

    score = 15

    debt = fundamental_data.get("debtEquity")
    profit_margin = fundamental_data.get("profitMargins")
    market_cap = fundamental_data.get("marketCap")

    risk_level = "🟢 Low"

    # High debt = higher risk
    if debt is not None:
        if debt > 200:
            score -= 6
        elif debt > 100:
            score -= 3

    # Low profit margin = higher risk
    if profit_margin is not None and profit_margin < 0.05:
        score -= 3

    # Small company = slightly risky
    if market_cap is not None and market_cap < 5_000_000_000:
        score -= 2

    score = max(score, 0)

    # Risk Level
    if score >= 12:
        risk_level = "🟢 Low"

    elif score >= 8:
        risk_level = "🟡 Moderate"

    else:
        risk_level = "🔴 High"

    return {
        "score": score,
        "riskLevel": risk_level,
        "debtEquity": debt,
        "profitMargins": profit_margin,
        "marketCap": market_cap,
    }