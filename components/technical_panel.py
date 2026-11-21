import streamlit as st


def render_technical_panel(technical):

    with st.sidebar:

        st.markdown("# 🚀 AlphaVision AI")
        st.caption("AI Powered Stock Analysis")

        st.divider()

        st.markdown("### 👤 User")
        st.success("Welcome, Abhinav")

        st.divider()

        st.markdown("### 📌 Navigation")

        st.page_link("app.py", label="🏠 Dashboard")

        st.page_link(
            "pages/1_Stock_Analysis.py",
            label="📈 Stock Analysis"
        )

        st.page_link(
            "pages/2_Screener.py",
            label="🔍 Screener"
        )

        st.page_link(
            "pages/4_Compare.py",
            label="⚖ Compare"
        )

        st.page_link(
            "pages/5_Reports.py",
            label="📄 Reports"
        )

        st.divider()

        st.markdown("### 📊 Market Status")

        st.success("🟢 Market Open")

        st.metric(
            "AI Accuracy",
            "91%"
        )

        st.metric(
            "Stocks Tracked",
            "500+"
        )