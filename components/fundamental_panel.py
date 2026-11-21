import streamlit as st


def render_fundamental_panel(fundamental):

    st.divider()
    st.markdown("## 🏢 Fundamental Analysis")

    c1, c2 = st.columns(2)

    # ==========================
    # Format Values
    # ==========================

    # ROE
    roe = fundamental.get("roe")
    if isinstance(roe, (int, float)):
        roe_text = f"{roe * 100:.2f}%"
    else:
        roe_text = "N/A"

    # EPS
    eps = fundamental.get("eps")
    if isinstance(eps, (int, float)):
        eps_text = f"₹ {eps:.2f}"
    else:
        eps_text = "N/A"

    # P/E
    pe = fundamental.get("pe")
    if isinstance(pe, (int, float)):
        pe_text = f"{pe:.2f}"
    else:
        pe_text = "N/A"

    # Debt / Equity
    debt = fundamental.get("debtEquity")
    if isinstance(debt, (int, float)):
        debt_text = f"{debt:.2f}"
    else:
        debt_text = "N/A"

    # Market Cap
    market_cap = fundamental.get("marketCap")

    if isinstance(market_cap, (int, float)):
        if market_cap >= 1e12:
            market_cap_text = f"₹ {market_cap / 1e12:.2f} T"
        elif market_cap >= 1e9:
            market_cap_text = f"₹ {market_cap / 1e9:.2f} B"
        elif market_cap >= 1e6:
            market_cap_text = f"₹ {market_cap / 1e6:.2f} M"
        else:
            market_cap_text = f"₹ {market_cap:,.0f}"
    else:
        market_cap_text = "N/A"

    # Profit Margin
    margin = fundamental.get("profitMargins")

    if isinstance(margin, (int, float)):
        margin_text = f"{margin * 100:.2f}%"
    else:
        margin_text = "N/A"

    # Dividend Yield
    dividend = fundamental.get("dividendYield")

    if isinstance(dividend, (int, float)):
        dividend_text = f"{dividend * 100:.2f}%"
    else:
        dividend_text = "N/A"

    # ==========================
    # UI
    # ==========================

    with c1:

        st.metric("ROE", roe_text)
        st.metric("EPS", eps_text)
        st.metric("Profit Margin", margin_text)

    with c2:

        st.metric("P/E Ratio", pe_text)
        st.metric("Debt / Equity", debt_text)
        st.metric("Market Cap", market_cap_text)
        st.metric("Dividend Yield", dividend_text)

    st.success(
        f"Overall Fundamental Score : {fundamental.get('score', 0)}/70"
    )

    st.info(
        """
### 📘 Fundamental Summary

- ✅ Higher ROE indicates efficient management.
- ✅ Lower Debt/Equity means lower financial risk.
- ✅ Healthy Profit Margin indicates good profitability.
- ✅ Dividend Yield benefits long-term investors.
- ✅ Large Market Cap companies are generally more stable.
        """
    )