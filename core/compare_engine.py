from core.data_fetcher import get_stock_chart
from core.fundamental import (
    get_fundamental_data,
    calculate_fundamental_score,
)
from core.technical import calculate_technical_score
from core.risk import calculate_risk_score
from core.valuation import calculate_valuation_score


def compare_stock(symbol):

    fundamental = get_fundamental_data(symbol)

    if not fundamental:
        return None

    chart = get_stock_chart(symbol)

    if chart is None or chart.empty:
        return None

    fundamental_result = calculate_fundamental_score(fundamental)

    technical_result = calculate_technical_score(chart)

    risk_result = calculate_risk_score(fundamental)

    valuation_result = calculate_valuation_score(fundamental)

    final_score = (
        fundamental_result["score"]
        + technical_result["score"]
        + risk_result["score"]
        + valuation_result["score"]
    )

    return {
    "Company": fundamental.get("company", symbol),
    "Current Price": fundamental.get("currentPrice", "-"),
    "PE": fundamental.get("pe", "-"),
    "PB": fundamental.get("pb", "-"),
    "ROE": fundamental.get("roe", "-"),
    "Debt": fundamental.get("debtEquity", "-"),

    "Fundamental": fundamental_result["score"],
    "Technical": technical_result["score"],
    "Risk": risk_result["score"],
    "Valuation": valuation_result["score"],

    "Score": final_score,
}