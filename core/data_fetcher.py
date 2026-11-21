import yfinance as yf
import pandas as pd


def get_stock_info(symbol):
    try:
        stock = yf.Ticker(symbol)

        info = stock.info

        data = {
            "symbol": symbol,
            "name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),

            "price": info.get("currentPrice"),
            "marketCap": info.get("marketCap"),

           "pe": info.get("trailingPE"),
           "pb": info.get("priceToBook"),

           "roe": info.get("returnOnEquity"),
           "debtEquity": info.get("debtToEquity"),

           "dividendYield": info.get("dividendYield"),
 
           "beta": info.get("beta"),

          "high52": info.get("fiftyTwoWeekHigh"),
          "low52": info.get("fiftyTwoWeekLow"),

          "volume": info.get("volume"),
          "avgVolume": info.get("averageVolume"),
        }

        return data

    except Exception as e:
        return None


def get_stock_chart(symbol, period="1y"):

    stock = yf.Ticker(symbol)

    df = stock.history(period=period)

    return df

def get_historical_data(symbol, period="1y"):

    stock = yf.Ticker(symbol)

    df = stock.history(period=period)

    df.reset_index(inplace=True)

    return df