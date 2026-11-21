from core.report_generator import generate_report
from core.pdf_generator import create_pdf
from core.ai_analyst import generate_ai_report, analyze_news_sentiment
from core.news_engine import get_stock_news
from components.sidebar import render_sidebar
import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Research Reports",
    page_icon="📄",
    layout="wide"
)
with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

render_sidebar()

st.title("📄 AlphaVision AI Research Report")
st.write("Generate a professional stock research report.")

symbol = st.text_input(
    "Enter Stock Symbol",
    value="RELIANCE.NS"
).upper()


if st.button("📊 Generate Report"):

    with st.spinner("Generating Report..."):
        report = generate_report(symbol)

    if report is None:

        st.error("Unable to fetch stock data.")

    else:

        # ==================================================
        # Report Generated
        # ==================================================

        st.success("✅ Report Generated Successfully")

        # ==================================================
        # AI Summary
        # ==================================================

        if st.button("🤖 Generate AI Summary"):

            with st.spinner("AI is analyzing the stock..."):

                summary = generate_ai_report(report)

            st.subheader("🤖 AI Investment Analyst")
            st.markdown(summary)

        # ==================================================
        # Company Information
        # ==================================================

        st.subheader("🏢 Company Information")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Company", report["Company"])
            st.metric("Symbol", report["Symbol"])
            st.metric("Current Price", report["Current Price"])

        with col2:
            st.metric("Recommendation", report["Recommendation"])
            st.metric("Final Score", f"{report['Score']} / 135")

        st.divider()

        # ==================================================
        # Financial Metrics
        # ==================================================

        st.subheader("📈 Financial Metrics")

        metrics = pd.DataFrame(
            {
                "Metric": [
                    "PE Ratio",
                    "PB Ratio",
                    "ROE",
                    "Debt / Equity",
                    "Fundamental Score",
                    "Technical Score",
                    "Risk Score",
                    "Valuation Score",
                ],
                "Value": [
                    report["PE"],
                    report["PB"],
                    report["ROE"],
                    report["Debt"],
                    report["Fundamental"],
                    report["Technical"],
                    report["Risk"],
                    report["Valuation"],
                ],
            }
        )

        st.dataframe(
            metrics,
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        # ==================================================
        # Investment Summary
        # ==================================================

        st.subheader("📋 Investment Summary")

        if report["Score"] >= 110:

            st.success("""
### 🟢 STRONG BUY

The company has strong fundamentals, healthy technical momentum,
reasonable valuation and low financial risk.

Suitable for long-term investors.
""")

        elif report["Score"] >= 90:

            st.info("""
### 🟡 BUY

The company looks fundamentally healthy with a good overall score.

Can be considered after proper risk management.
""")

        elif report["Score"] >= 70:

            st.warning("""
### 🟠 WATCHLIST

The company has mixed signals.

Wait for better valuation or technical confirmation.
""")

        else:

            st.error("""
### 🔴 AVOID

The company currently does not satisfy AlphaVision AI screening criteria.

Avoid fresh investment until conditions improve.
""")

        st.divider()

        # ==================================================
        # Latest News
        # ==================================================

        st.subheader("📰 Latest Company News")

        news = get_stock_news(symbol)

        if news:

            for article in news:

                st.markdown(f"### {article['title']}")

                if article["publisher"]:
                    st.caption(f"Source: {article['publisher']}")

                if article["link"]:
                    st.markdown(f"[🔗 Read Full Article]({article['link']})")

                st.markdown("---")

            if st.button("🤖 Analyze News Sentiment"):

                with st.spinner("Analyzing latest news..."):

                    sentiment = analyze_news_sentiment(news)

                st.subheader("📊 AI News Sentiment")
                st.markdown(sentiment)

        else:

            st.info("No recent news found for this stock.")

        st.divider()

        # ==================================================
        # PDF Download
        # ==================================================

        pdf_file = f"{report['Symbol']}_Research_Report.pdf"

        create_pdf(report, pdf_file)

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="📥 Download PDF Report",
                data=file,
                file_name=pdf_file,
                mime="application/pdf",
            )

        if os.path.exists(pdf_file):
            os.remove(pdf_file)