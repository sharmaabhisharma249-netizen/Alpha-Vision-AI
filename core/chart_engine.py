import yfinance as yf
import plotly.graph_objects as go


def get_stock_chart(symbol):

    df = yf.download(symbol, period="1y", interval="1d")

    if df.empty:
        return None

    df["EMA50"] = df["Close"].ewm(span=50).mean()
    df["EMA200"] = df["Close"].ewm(span=200).mean()

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["EMA50"],
            mode="lines",
            name="EMA 50",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["EMA200"],
            mode="lines",
            name="EMA 200",
        )
    )

    fig.update_layout(
        title=f"{symbol} Price Chart",
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Price",
        height=700,
        xaxis_rangeslider_visible=False,
    )

    return fig