from core.data_fetcher import (
    get_stock_info,
    get_historical_data
)
from core.technical import calculate_technical_score
from core.fundamental import (
    get_fundamental_data,
    calculate_fundamental_score
)
from core.risk import calculate_risk_score
from auth.auth_utils import (
    add_to_watchlist,
    remove_from_watchlist,
    get_watchlist
)
from core.valuation import calculate_valuation_score
from core.scoring import calculate_final_score
from core.news_engine import get_stock_news
from core.ai_analyst import analyze_news_sentiment
from core.ai_chat import ask_ai
from components.company_header import render_company_header
from core.chart import get_candlestick_chart
from components.score_cards import render_score_cards
from components.price_chart import render_price_chart
from components.technical_panel import render_technical_panel
from components.fundamental_panel import render_fundamental_panel
from components.risk_panel import render_risk_panel
from components.valuation_panel import render_valuation_panel
from components.ai_recommendation import render_ai_recommendation
from components.sidebar import render_sidebar

import streamlit as st
# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Stock Analysis",
    page_icon="📈",
    layout="wide"
)
with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
render_sidebar()
st.title("📈 AlphaVision AI")

st.write(
    "AI Powered Stock Analysis Platform"
)

# ==========================================
# STOCK INPUT
# ==========================================

symbol = st.text_input(
    "Enter NSE Stock Symbol",
    value="RELIANCE.NS"
).upper()

# ==========================================
# ANALYZE BUTTON
# ==========================================

if st.button("🚀 Analyze Stock"):

    with st.spinner("Analyzing Stock..."):

        info = get_stock_info(symbol)

        history = get_historical_data(symbol)
        render_company_header(info)

        if info is None or history.empty:

            st.error("Unable to fetch stock data.")

            st.stop()

        chart = get_candlestick_chart(symbol)

        technical = calculate_technical_score(
            history
        )

        fundamental_data = get_fundamental_data(
            symbol
        )

        fundamental = calculate_fundamental_score(
            fundamental_data
        )

        risk = calculate_risk_score(
            fundamental_data
        )

        valuation = calculate_valuation_score(
            fundamental_data
        )

        final = calculate_final_score(
            fundamental,
            technical,
            risk,
            valuation
        )

        # ==========================
        # NEWS
        # ==========================

        news = get_stock_news(symbol)

        sentiment = analyze_news_sentiment(
            news
        )

        # ==========================
        # SAVE SESSION
        # ==========================

        st.session_state["info"] = info
        st.session_state["chart"] = chart
        st.session_state["technical"] = technical
        st.session_state["fundamental"] = fundamental
        st.session_state["risk"] = risk
        st.session_state["valuation"] = valuation
        st.session_state["final"] = final
        st.session_state["news"] = news
        st.session_state["sentiment"] = sentiment

# ==========================================
# LOAD SESSION
# ==========================================

if "info" in st.session_state:

    info = st.session_state["info"]

    chart = st.session_state["chart"]

    technical = st.session_state["technical"]

    fundamental = st.session_state["fundamental"]

    risk = st.session_state["risk"]

    valuation = st.session_state["valuation"]

    final = st.session_state["final"]

    news = st.session_state["news"]

    sentiment = st.session_state["sentiment"]
       
    # ==========================================
    # PREMIUM HERO SECTION
    # ==========================================

    st.markdown("""
    <style>

    .hero-card{
    background:linear-gradient(135deg,#0F172A,#111827);
    padding:30px;
    border-radius:20px;
    border:1px solid #1F2937;
    margin-bottom:20px;
    box-shadow:0px 8px 25px rgba(0,0,0,.35);
    }

    .small-card{
    background:#111827;
    padding:18px;
    border-radius:16px;
    border:1px solid #1F2937;
    text-align:center;
    box-shadow:0px 6px 15px rgba(0,0,0,.25);
    }

    .buy-badge{
    background:#16A34A;
    padding:8px 18px;
    border-radius:30px;
    color:white;
    font-weight:bold;
    display:inline-block;
    }

    .hold-badge{
    background:#F59E0B;
    padding:8px 18px;
    border-radius:30px;
    color:white;
    font-weight:bold;
    display:inline-block;
    }

    .sell-badge{
    background:#DC2626;
    padding:8px 18px;
    border-radius:30px;
    color:white;
    font-weight:bold;
    display:inline-block;
    }

    </style>
    """, unsafe_allow_html=True)

    score = final["final_score"]
    recommendation = final["recommendation"]

    if "STRONG BUY" in recommendation.upper():
        badge = "<span class='buy-badge'>🚀 STRONG BUY</span>"
    
    elif "BUY" in recommendation.upper():
        badge = "<span class='buy-badge'>🟢 BUY</span>"
    
    elif "HOLD" in recommendation.upper():
        badge = "<span class='hold-badge'>🟡 HOLD</span>"
    
    else:
        badge = "<span class='sell-badge'>🔴 SELL</span>"
    
    st.markdown(
        f"""
    <div class="hero-card">
    
    <h1 style="margin-bottom:0px;color:#00E5FF;">
    {info.get("name","N/A")}
    </h1>
    
    <h3 style="margin-top:10px;">
    ₹ {info.get("price","N/A")}
    </h3>
    
    {badge}
    
    <h3 style="margin-top:20px;">  
    ⭐ AlphaVision Score : {score}/140
       </h3>
    
    </div>
    """,
        unsafe_allow_html=True
    )

    st.write("")
    user = st.session_state["user"]

    watchlist = get_watchlist(user["id"])

    symbols = [
        item["symbol"]
        for item in watchlist
    ]

    if symbol in symbols:

        if st.button(
            "💔 Remove from Watchlist",
            use_container_width=True
        ):

            remove_from_watchlist(
                user["id"],
                symbol
            )

            st.success(
                "Removed from Watchlist"
            )

            st.rerun()

    else:

        if st.button(
            "⭐ Add to Watchlist",
            use_container_width=True
        ):

            add_to_watchlist(
                user["id"],
                symbol,
                info.get("name")
            )

            st.success(
                "Added to Watchlist"
            )

            st.rerun()

# ==========================================
# QUICK METRICS
# ==========================================

    render_score_cards(
    technical,
    fundamental,
    valuation,
    risk
)

    render_price_chart(chart)

# ==========================================
# TECHNICAL ANALYSIS
# ==========================================

    render_technical_panel(technical)

# ==========================================
# FUNDAMENTAL ANALYSIS
# ==========================================

    render_fundamental_panel(fundamental)
    

# ==========================================
# RISK ANALYSIS
# ==========================================

    render_risk_panel(risk)

    # ==========================================
    # VALUATION ANALYSIS
    # ==========================================

    render_valuation_panel(valuation)

# ==========================================
# FINAL SCORE
# ==========================================

    st.divider()

    st.subheader("⭐ AlphaVision AI Overall Score")

    score = final["final_score"]

    recommendation = final["recommendation"]

    st.metric(
        "Overall Score",
        f"{score} / 140"
    )

    st.progress(min(score / 140, 1.0))

# ==========================================
# AI RECOMMENDATION
# ==========================================

    render_ai_recommendation(
        recommendation,
        score,
        technical,
        fundamental,
        risk,
        sentiment
    )


# ==========================================
# ANALYSIS SUMMARY
# ==========================================

    st.divider()

    st.subheader("📋 Analysis Summary")
    # ===== Format Values =====

    roe = fundamental.get("roe")
    roe_text = f"{roe * 100:.2f}%" if isinstance(roe, (int, float)) else "N/A"

    margin = fundamental.get("profitMargins")
    margin_text = f"{margin * 100:.2f}%" if isinstance(margin, (int, float)) else "N/A"

    pe = fundamental.get("pe")
    pe_text = f"{pe:.2f}" if isinstance(pe, (int, float)) else "N/A"

    st.markdown(f"""
### 🏢 Company
**{info.get("name", "N/A")}**

---

### 📊 Technical Analysis

- **RSI:** {technical["rsi"]}
- **Trend:** {technical["trend"]}
- **Technical Score:** {technical["score"]}/20

---

### 🏢 Fundamental Analysis

- - **P/E Ratio:** {pe_text}

- **ROE:** {roe_text}

- **Profit Margin:** {margin_text}
- **Fundamental Score:** {fundamental["score"]}/70

---

### ⚠️ Risk Analysis

- **Risk Level:** {risk["riskLevel"]}
- **Risk Score:** {risk["score"]}/15

---

### 💰 Valuation

- **Status:** {valuation["valuation"]}
- **Valuation Score:** {valuation["score"]}/30

---

# ⭐ Overall Score: **{score}/140**

# 🤖 Recommendation: **{recommendation}**
""")

# ==========================================
# AI NEWS SENTIMENT
# ==========================================

    st.divider()

    st.subheader("🧠 AI News Sentiment")

    sentiment_lower = sentiment.strip().lower()

    if "positive" in sentiment_lower:

        st.success(f"🟢 {sentiment}")

    elif "negative" in sentiment_lower:

        st.error(f"🔴 {sentiment}")

    else:

        st.warning(f"🟡 {sentiment}")

# ==========================================
# LATEST STOCK NEWS
# ==========================================

    st.divider()

    st.subheader("📰 Latest Stock News")

    if not news:

        st.info("No recent news available.")

    else:

        for item in news:

            st.markdown(f"### 📰 {item.get('title', 'No Title')}")

            st.write(
                f"**Publisher:** {item.get('publisher', 'Unknown')}"
            )

            link = item.get("link", "")

            if link:

                st.markdown(
                    f"[🔗 Read Full Article]({link})"
                )

            st.divider()
                # ==========================================
    # AI CHAT
    # ==========================================

    st.divider()

    st.subheader("🤖 Ask AlphaVision AI")

    question = st.text_area(
        "Ask anything about this stock",
        placeholder="Example: Should I buy this stock for long-term?"
    )

    if st.button("🤖 Ask AI"):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            stock_data = {

                "company": info.get("name", symbol),

                "symbol": symbol,

                "price": info.get("price", "N/A"),

                "technical_score": technical["score"],

                "fundamental_score": fundamental["score"],

                "risk_score": risk["score"],

                "risk_level": risk["riskLevel"],

                "valuation": valuation["valuation"],

                "valuation_score": valuation["score"],

                "overall_score": score,

                "recommendation": recommendation,

                "rsi": technical["rsi"],

                "trend": technical["trend"],

                "pe": fundamental["pe"],

                "roe": fundamental["roe"],

                "profit_margin": fundamental["profitMargins"],

                "debt_equity": fundamental["debtEquity"],

                "news_sentiment": sentiment,

                "latest_news": news

            }

            with st.spinner("🤖 AlphaVision AI is analyzing..."):

                answer = ask_ai(
                    question,
                    stock_data
                )

            st.success("### 🤖 AI Answer")

            st.write(answer)

# ==========================================
# FOOTER
# ==========================================

    st.divider()

    st.caption(
        "Made with ❤️ using Streamlit • Plotly • Yahoo Finance • Google News • Gemini AI"
    )
        