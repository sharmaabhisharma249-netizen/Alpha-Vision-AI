from core.nse_stocks import load_nse_stocks
from core.chart import get_stock_chart

from core.fundamental import (
    get_fundamental_data,
    calculate_fundamental_score,
)

from core.technical import calculate_technical_score
from core.risk import calculate_risk_score
from core.valuation import calculate_valuation_score
import traceback
import pandas as pd
print("############ NEW FILE LOADED ############")
def run_screener(progress_callback=None, search=""):
    print("SEARCH PARAM =", search)

    stocks = load_nse_stocks()
    if search.strip():
        stocks = stocks[
            stocks["Company"].str.contains(
                search,
                case=False,
                na=False
            )
        ]
    else:
        stocks = stocks.head(25)
    total_stocks = len(stocks)
    if total_stocks == 0:
        return pd.DataFrame()

    results = []
    if search.strip():

        stocks = stocks[
            stocks["Company"].str.contains(search, case=False, na=False)
            |
            stocks["Symbol"].str.contains(search, case=False, na=False)
        ]
    if total_stocks == 0:
        return pd.DataFrame()   
    total_stocks = len(stocks)
    print("Search:", search)
    print("Stocks after search:", len(stocks))
    print(stocks[["Company", "Symbol"]].head())

    for index, (_, row) in enumerate(stocks.iterrows(), start=1):
        # Update Progress
        if progress_callback:
            progress_callback(index, total_stocks)

        symbol = row["Symbol"]
        company = row["Company"]
        sector = row["Sector"]

        print(f"Processing {index}/{total_stocks} : {symbol}")

        print(f"\nProcessing: {symbol}")

        try:

            # ----------------------------
            # Fundamental Data
            # ----------------------------

            fundamental = get_fundamental_data(symbol)
            print("Fundamental:", fundamental)
            print("Fundamental fetched")  

            if not fundamental:
                continue
            

            # ----------------------------
            # Price Data
            # ----------------------------

            df = get_stock_chart(symbol)
            print("Chart Rows:", 0 if df is None else len(df))
            print("History rows:", 0 if df is None else len(df))
            print("Chart Empty:", df is None or df.empty)

            if df is None or df.empty:
                continue

            # ----------------------------
            # Individual Scores
            # ----------------------------

            fundamental_result = calculate_fundamental_score(
                fundamental
            )

            technical_result = calculate_technical_score(
                df
            )

            risk_result = calculate_risk_score(
                fundamental
            )

            valuation_result = calculate_valuation_score(
                fundamental
            )

            # ----------------------------
            # Final Score
            # ----------------------------

            final_score = (
                fundamental_result["score"]
                + technical_result["score"]
                + risk_result["score"]
                + valuation_result["score"]
            )

            # ----------------------------
            # Recommendation
            # ----------------------------

            fundamental_score = fundamental_result["score"]
            technical_score = technical_result["score"]

            if fundamental_score >= 60 and technical_score >= 12:

                if final_score >= 110:
                    recommendation = "🟢 STRONG BUY"
                else:
                    recommendation = "🟡 BUY"

            elif fundamental_score < 55 and technical_score < 10:

                recommendation = "🔴 AVOID"

            else:

                recommendation = "🟠 WATCHLIST"
            # ----------------------------
            # Save Result
            # ----------------------------

            results.append(
               {
                    "Symbol": symbol,
                    "Company": company,
                    "Sector": sector,
                    "PE": fundamental.get("pe", "-"),
                    "PB": fundamental.get("pb", "-"),
                    "ROE": fundamental.get("roe", "-"),
                    "Debt": fundamental.get("debtEquity", "-"),
                    "Fundamental": fundamental_result["score"],
                    "Technical": technical_result["score"],
                    "Risk": risk_result["score"],
                    "Valuation": valuation_result["score"],
                    "Score": final_score,
                    "Recommendation": recommendation,
               }
           )
        except Exception:
            traceback.print_exc()
            continue    
        print("=" * 50)
        print("Total Results:", len(results))

    if len(results) > 0:
        print(pd.DataFrame(results).head())
    else:
        print("Results list is EMPTY")

    return pd.DataFrame(results) 