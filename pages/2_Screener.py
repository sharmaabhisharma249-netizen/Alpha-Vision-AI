from core.screener_engine import run_screener
from components.sidebar import render_sidebar
from core.nse_stocks import load_nse_stocks
from core.chart import get_candlestick_chart
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def safe_value(value, digits=2, percent=False):

    if value is None:
        return "N/A"

    if pd.isna(value):
        return "N/A"

    try:
        if percent:
            return f"{round(value * 100, digits)}%"

        return round(value, digits)

    except:
        return "N/A"
st.set_page_config(
    page_title="AlphaVision AI - Screener",
    page_icon="🔍",
    layout="wide"
)

render_sidebar()

with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.title("🔍 Advanced Stock Screener")
st.write("Scan NSE Stocks using AlphaVision AI")

# ==================================================
# FILTER PANEL
# ==================================================

stock_df = load_nse_stocks()

sector_options = ["All"] + sorted(
    stock_df["Sector"].dropna().unique().tolist()
)

st.markdown("## 🎯 Filters")

col1, col2 = st.columns(2)

with col1:
    search = st.text_input(
        "🔎 Search Company",
        placeholder="e.g. Reliance"
    )
    single_company = search.strip() != ""

with col2:
    selected_sector = st.selectbox(
        "🏭 Sector",
        sector_options,
        disabled=single_company
    )

col3, col4 = st.columns(2)

with col3:
    min_score = st.slider(
        "⭐ Minimum Score",
        min_value=0,
        max_value=135,
        value=90,
        disabled=single_company
    )

with col4:
    recommendation = st.selectbox(
    "Recommendation",
    [
        "All",
        "🟢 STRONG BUY",
        "🟡 BUY",
        "🟠 WATCHLIST",
        "🔴 AVOID"
    ]
    , disabled=single_company
)
st.divider()

# ==================================================
# SCORE COLORS
# ==================================================

def color_score(val):
    if val >= 110:
        return "background-color:#00AA00; color:white;"
    elif val >= 90:
        return "background-color:#FFA500; color:black;"
    else:
        return "background-color:#AA0000; color:white;"

# ==================================================
# RUN SCREENER
# ==================================================

run = st.button(
    "🚀 Run Screener",
    use_container_width=True
)

if run:

    progress_bar = st.progress(0)
    status = st.empty()

    def update_progress(current, total):
        progress_bar.progress(current / total)
        status.info(f"🔄 Scanning Stock {current} of {total}...")

    with st.spinner("Scanning NSE Stocks..."):
        df = run_screener(
            progress_callback=update_progress,
            search=search
        )
    progress_bar.empty()
    status.empty()
    
    if df.empty:
        st.warning("No matching stocks found.")
        st.stop()
    # Sort by Score
    df = df.sort_values("Score", ascending=False)

    # Minimum Score Filter
    if not single_company:

        df = df[df["Score"] >= min_score]

        if selected_sector != "All":
            df = df[df["Sector"] == selected_sector]

        if recommendation != "All":
            df = df[df["Recommendation"] == recommendation]

    # ===============================
    # Summary Cards
    # ===============================

    total_stocks = len(df)
    buy_count = (df["Recommendation"] == "🟢 STRONG BUY").sum()
    avg_score = round(df["Score"].mean(), 1) if not df.empty else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📈 Stocks Found", total_stocks)

    with col2:
        st.metric("⭐ Avg Score", avg_score)

    with col3:
        st.metric("🟢 Buy Signals", buy_count)

    st.success(f"✅ {len(df)} Stocks Found")

    if df.empty:
        st.warning("No stocks matched your filters.")

    else:

        styled = df.style.map(
            color_score,
            subset=["Score"]
        )

        # ===============================
        # Export CSV
        # ===============================

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Export Results as CSV",
            data=csv,
            file_name="AlphaVision_Screener.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.dataframe(
            styled,
            use_container_width=True
        )
        
        sector_data = (
            df["Sector"]
            .value_counts()
            .reset_index()
        )

        sector_data.columns = [
           "Sector",
           "Stocks"
        ]
        

        with st.container(border=True):

            st.subheader("📊 Market Analytics")
            
            col1, col2 = st.columns(2)

            # -------------------------
            # Donut Chart
            # -------------------------

            with col1:

                st.subheader("🍩 Sector Distribution")

                fig = px.pie(
                    sector_data,
                    names="Sector",
                    values="Stocks",
                    hole=0.45,
                    title="Stocks by Sector"
                )
                fig.update_layout(
                    height=350
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # -------------------------
            # Bar Chart
            # -------------------------

            with col2:

                st.subheader("📊 Sector-wise Stock Count")

                bar_fig = px.bar(
                    sector_data,
                    x="Sector",
                    y="Stocks",
                    text="Stocks",
                    title="Stocks per Sector"
                )

                bar_fig.update_layout(
                    xaxis_title="Sector",
                    yaxis_title="Number of Stocks",
                    height=350
                )

                st.plotly_chart(
                    bar_fig,
                    use_container_width=True
                )

                

            col3, col4 = st.columns(2)

            with col3:

                st.subheader("📈 Score Distribution")

                hist_fig = px.histogram(
                    df,
                    x="Score",
                    nbins=10,
                    title="Distribution of Stock Scores"
                )

                hist_fig.update_layout(
                    xaxis_title="Score",
                    yaxis_title="Number of Stocks",
                    height=350
                )

                st.plotly_chart(
                    hist_fig,
                    use_container_width=True
                )

              
                # ===============================
    # Recommendation Distribution
    # ===============================
            with col4:

                st.subheader("🎯 Recommendation Distribution")

                recommendation_data = (
                    df["Recommendation"]
                    .value_counts()
                    .reset_index()
                )

                recommendation_data.columns = [
                    "Recommendation",
                    "Count"
                ]

                recommendation_fig = px.pie(
                    recommendation_data,
                    names="Recommendation",
                    values="Count",
                    hole=0.45,
                    title="Recommendation Distribution"
                )
                recommendation_fig.update_layout(
                    height=350
                )

                st.plotly_chart(
                    recommendation_fig,
                    use_container_width=True
                )

               
            # ==========================================
# 🏆 TOP 5 STOCKS
# ==========================================

            st.subheader("🏆 Top 5 Stocks")

            top5 = df.sort_values("Score", ascending=False).head(5)

            for _, row in top5.iterrows():

                pe = safe_value(row.get("PE"))
                pb = safe_value(row.get("PB"))
                roe = safe_value(row.get("ROE"), percent=True)
                debt = safe_value(row.get("Debt"))
                score = safe_value(row.get("Score"), 0)

                recommendation = row.get("Recommendation", "N/A")
                company = row.get("Company", "N/A")
                symbol = row.get("Symbol", "N/A")
                sector = row.get("Sector", "N/A")

                st.markdown(
                    f"""
            <div style="
            background:#111827;
            padding:18px;
            border-radius:12px;
            border:1px solid #2A2F3A;
            margin-bottom:15px;
            ">

            <h4 style="margin-bottom:10px;">
            {company}
            </h4>

            <b>{symbol}</b>

            <hr>

            <p>🏢 <b>Sector:</b> {sector}</p>

            <p>💰 <b>PE:</b> {pe}</p>

            <p>📊 <b>PB:</b> {pb}</p>

            <p>📈 <b>ROE:</b> {roe}</p>

            <p>🏦 <b>Debt/Equity:</b> {debt}</p>

            <p>🏆 <b>Score:</b> {score}</p>

            <p><b>{recommendation}</b></p>

            </div>
            """,
                    unsafe_allow_html=True,
                )
      
            st.divider()


        with st.container(border=True):

            st.markdown("### 🔍 Stock Detail Analysis")

            selected_stock = st.selectbox(
                "Select a Stock",
                sorted(df["Company"].unique())
            )

            stock_data = df[df["Company"] == selected_stock].iloc[0]
            chart = get_candlestick_chart(
            stock_data["Symbol"]
            )
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("⭐ Score", stock_data["Score"])
            rec = stock_data["Recommendation"]

            if rec in ["BUY", "STRONG BUY"]:
                badge_class = "badge-buy"
                icon = "🟢"
            elif rec == "WATCHLIST":
                badge_class = "badge-hold"
                icon = "🟡"
            else:
                badge_class = "badge-sell"
                icon = "🔴"

            col2.markdown("#### 📊 Recommendation")
            col2.markdown(
                f"""
                <div class="{badge_class}">
                    {icon} {rec}
                </div>
                """,
                unsafe_allow_html=True
            )
            col3.metric("🏭 Sector", stock_data["Sector"])
            col4.metric("💰 PE", round(stock_data["PE"], 2))

            st.subheader("📈 Candlestick Chart")

            st.plotly_chart(
                chart,
                use_container_width=True
            )
            st.markdown("---")
            st.markdown(
                '<div class="section-title">📊 Fundamental Analysis</div>',
                unsafe_allow_html=True
            )

            left, right = st.columns(2)

            with left:
                roe = stock_data.get("ROE")

                st.metric(
                    "📈 ROE",
                    f"{round(roe * 100, 2)}%" if roe is not None else "N/A"
                )
                pe = stock_data.get("PE")

                st.metric(
                    "💰 PE Ratio",
                    round(pe, 2) if pe is not None else "N/A"
                )

            with right:
                pb = stock_data.get("PB")

                st.metric(
                    "📊 PB Ratio",
                    round(pb, 2) if pb is not None else "N/A"
                )
                debt = stock_data.get("Debt")

                st.metric(
                    "🏦 Debt / Equity",
                    round(debt, 2) if debt is not None else "N/A"
                )

            st.metric("⭐ Fundamental Score", f'{stock_data["Fundamental"]}/70')


            st.markdown("---")
            st.subheader("📈 Technical Analysis")

            left, right = st.columns(2)

            with left:
                st.metric("📊 Technical Score", f'{stock_data["Technical"]}/35')
                st.metric("💎 Valuation Score", f'{stock_data["Valuation"]}/25')

            with right:
                st.metric("⚖️ Risk Score", f'{stock_data["Risk"]}/25')
                st.metric("🟢 Recommendation", stock_data["Recommendation"])
            st.markdown("---")
            st.markdown(
                '<div class="section-title">📊 Overall Score Breakdown</div>',
                unsafe_allow_html=True
            )

            score = stock_data["Score"]

            # Rating & Gauge Color
            if score >= 110:
                rating = "🏆 Excellent"
                gauge_color = "#22C55E"
            elif score >= 90:
                rating = "🟢 Good"
                gauge_color = "#3B82F6"
            elif score >= 60:
                rating = "🟡 Average"
                gauge_color = "#F59E0B"
            else:
                rating = "🔴 Weak"
                gauge_color = "#EF4444"

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                number={
                    "suffix": " / 135",
                    "font": {"size": 34}
                },
                title={
                    "text": "<b>Overall Score</b>",
                    "font": {"size": 22}
                },
                gauge={
                    "axis": {
                        "range": [0, 135],
                        "tickwidth": 1,
                        "tickcolor": "#94A3B8"
                    },
                    "bar": {
                        "color": gauge_color,
                        "thickness": 0.35
                    },
                    "bgcolor": "white",
                    "borderwidth": 2,
                    "bordercolor": "#1F2937",
                    "steps": [
                        {"range": [0, 45], "color": "#FEE2E2"},
                        {"range": [45, 90], "color": "#FEF3C7"},
                        {"range": [90, 135], "color": "#DCFCE7"}
                    ],
                    "threshold": {
                        "line": {"color": "#111827", "width": 5},
                        "thickness": 0.8,
                        "value": score
                    }
                }
            ))

            fig.update_layout(
                height=340,
                margin=dict(l=20, r=20, t=40, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white")
            )

            st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    font-size:20px;
                    font-weight:700;
                    color:#00E5FF;
                    margin-top:-10px;
                    margin-bottom:20px;">
                    {rating}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Fundamental
            st.write(f"**📘 Fundamental** ({stock_data['Fundamental']}/70)")
            st.progress(min(stock_data["Fundamental"] / 70, 1.0))

            # Technical
            st.write(f"**📈 Technical** ({stock_data['Technical']}/20)")
            st.progress(min(stock_data["Technical"] / 20, 1.0))

            # Valuation
            st.write(f"**💎 Valuation** ({stock_data['Valuation']}/30)")
            st.progress(min(stock_data["Valuation"] / 30, 1.0))

            # Risk
            st.write(f"**⚖️ Risk** ({stock_data['Risk']}/15)")
            st.progress(min(stock_data["Risk"] / 15, 1.0))

            st.markdown("---")
            st.subheader("🤖 AlphaVision AI Insight")

            rec = stock_data["Recommendation"]

            if rec == "STRONG BUY":
                insight = (
                    "This stock performs exceptionally well across the AlphaVision AI framework. "
                    "It demonstrates strong fundamentals, healthy technical momentum, attractive valuation, "
                    "and acceptable risk levels. It qualifies as a Strong Buy candidate."
                )

            elif rec == "BUY":
                insight = (
                    "This stock satisfies most of the AlphaVision AI screening criteria. "
                    "It has solid fundamentals and technical strength with manageable risk, "
                    "making it suitable for further investment consideration."
                )

            elif rec == "WATCHLIST":
                insight = (
                    "This stock shows mixed signals. Investors should monitor its fundamentals "
                    "and technical trend before making an investment decision."
                )

            else:
                insight = (
                    "This stock does not currently satisfy the AlphaVision AI framework. "
                    "Weak fundamentals, technical weakness or elevated risk reduce its attractiveness."
                )

            st.info(insight)
            st.markdown("---")
            st.subheader("🧠 AlphaVision AI Scoring Framework")

            st.info("""
            ### 📊 Overall Score = 135 Points

            #### 📘 Fundamental Analysis (70 Points)
            - PE Ratio → 10 Points
            - Return on Equity (ROE) → 15 Points
            - Debt to Equity → 15 Points
            - Profit Margin → 15 Points
            - Market Capitalization → 15 Points

            #### 📈 Technical Analysis (20 Points)
            - Price above EMA50 → 5 Points
            - EMA50 above EMA200 → 5 Points
            - Healthy RSI (45–65) → 5 Points
            - Positive Momentum → 5 Points

            #### 💎 Valuation Analysis (30 Points)
            - Base Valuation Score → 20 Points
            - Attractive P/E Ratio → +5 Points
            - Attractive P/B Ratio → +5 Points

            #### ⚖️ Risk Assessment (15 Points)
            - Base Risk Score → 15 Points
            - High Debt → Penalty
            - Low Profit Margin → Penalty
            - Small Market Capitalization → Penalty

            🏆 **Final Score = Fundamental + Technical + Valuation + Risk (Maximum = 135)**
            """)