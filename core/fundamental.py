import yfinance as yf


def get_fundamental_data(symbol):

    stock = yf.Ticker(symbol)
    info = stock.info

    return {
        "company": info.get("longName"),
        "marketCap": info.get("marketCap"),
        "pe": info.get("trailingPE"),
        "pb": info.get("priceToBook"),
        "roe": info.get("returnOnEquity"),
        "debtEquity": info.get("debtToEquity"),
        "eps": info.get("trailingEps"),
        "bookValue": info.get("bookValue"),
        "dividendYield": info.get("dividendYield"),
        "profitMargins": info.get("profitMargins"),
    }


def calculate_fundamental_score(data):

    score = 0

    pe = data.get("pe")
    roe = data.get("roe")
    debt = data.get("debtEquity")
    margin = data.get("profitMargins")
    market_cap = data.get("marketCap")

    # PE Ratio
    if pe is not None and pe < 25:
        score += 10

    # ROE
    if roe is not None and roe > 0.15:
        score += 15

    # Debt to Equity
    if debt is not None and debt < 100:
        score += 15

    # Profit Margin
    if margin is not None and margin > 0.10:
        score += 15

    # Market Cap
    if market_cap is not None and market_cap > 10_000_000_000:
        score += 15

    return {
        "score": score,
        "pe": pe,
        "pb": data.get("pb"),
        "roe": roe,
        "debtEquity": debt,
        "eps": data.get("eps"),
        "bookValue": data.get("bookValue"),
        "dividendYield": data.get("dividendYield"),
        "profitMargins": margin,
        "marketCap": market_cap,
    }