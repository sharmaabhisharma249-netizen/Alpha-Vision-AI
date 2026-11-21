"""
=========================================
AlphaVision AI
Market Data Engine
=========================================
"""

import logging
from datetime import datetime, time


import pandas as pd
import streamlit as st
import yfinance as yf

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

INDEX_SYMBOLS = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN",
    "BANKNIFTY": "^NSEBANK",
    "MIDCAP": "^NSEMDCP50",
    "INDIA VIX": "^INDIAVIX"
}

def is_market_open():

    now = datetime.now()

    if now.weekday() >= 5:
        return False

    return time(9, 15) <= now.time() <= time(15, 30)


@st.cache_data(ttl=10)
def get_market_indices():

    market = {}

    for name, symbol in INDEX_SYMBOLS.items():

        try:

            stock = yf.Ticker(symbol)

            history = stock.history(period="5d", auto_adjust=True)
            print(f"Checking {symbol}")
            print(history.tail())
            if history.empty or len(history) < 2:
                raise ValueError("No Data")

            current = float(history["Close"].iloc[-1])

            previous = float(history["Close"].iloc[-2])

            change = current - previous
            percent = (change / previous) * 100

            market[name] = {
                "price": round(current, 2),
                "change": round(change, 2),
                "percent": round(percent, 2)
            }

        except Exception as e:
            print(f"ERROR {symbol}: {e}")
            market[name] = {
                "price": None,
                "change": None,
                "percent": None
            }

    return market


def get_market_sentiment():

    data = get_market_indices()

    bullish = sum(
        1 for v in data.values()
        if v["change"] is not None and v["change"] > 0
    )

    if bullish >= 4:
        mood = "🟢 Bullish"
        score = 90

    elif bullish >= 2:
        mood = "🟡 Neutral"
        score = 60

    else:
        mood = "🔴 Bearish"
        score = 30

    return {
        "mood": mood,
        "score": score
    }


def get_dashboard_summary():

    return {
        "indices": get_market_indices(),
        "sentiment": get_market_sentiment(),
        "market_open": is_market_open()
    }