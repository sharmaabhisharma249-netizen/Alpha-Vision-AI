import pandas as pd


def calculate_rsi(close, period=14):
    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_technical_score(df):

    df = df.copy()

    # Indicators
    df["EMA50"] = df["Close"].ewm(span=50).mean()
    df["EMA200"] = df["Close"].ewm(span=200).mean()
    df["RSI"] = calculate_rsi(df["Close"])

    latest = df.iloc[-1]

    score = 0

    # Price above EMA50
    if latest["Close"] > latest["EMA50"]:
        score += 5

    # Golden Trend
    if latest["EMA50"] > latest["EMA200"]:
        score += 5

    # Healthy RSI
    if 45 <= latest["RSI"] <= 65:
        score += 5

    # Momentum
    if len(df) >= 5 and latest["Close"] > df["Close"].iloc[-5]:
        score += 5

    # Trend
    trend = "🟢 Bullish"

    if latest["EMA50"] < latest["EMA200"]:
        trend = "🔴 Bearish"

    return {
        "score": score,
        "rsi": round(latest["RSI"], 2),
        "ema50": round(latest["EMA50"], 2),
        "ema200": round(latest["EMA200"], 2),
        "trend": trend,
    }