import yfinance as yf
import plotly.graph_objects as go


def get_stock_chart(symbol, period="1y"):

    df = yf.download(
        symbol,
        period=period,
        interval="1d",
        auto_adjust=False,
        progress=False
    )

    if df.empty:
        return None

    # MultiIndex handle
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)

    return df


def get_candlestick_chart(symbol, period="6mo", interval="1d"):

    df = yf.download(
        symbol,
        period=period,
        interval=interval,
        auto_adjust=False,
        progress=False
    )

    if df.empty:
        return go.Figure()

    # MultiIndex handle
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="Price"
            )
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        height=550,
        xaxis_rangeslider_visible=False,
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=20, b=20),
    )

    return fig