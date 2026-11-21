from core.compare_engine import compare_stock
from components.sidebar import render_sidebar
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Compare Stocks",
    page_icon="⚖️",
    layout="wide"
)
with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
render_sidebar()

st.title("⚖️ Compare Stocks")
st.write("Compare two stocks side by side using AlphaVision AI")

# ------------------------
# Inputs
# ------------------------

col1, col2 = st.columns(2)

with col1:
    stock1 = st.text_input(
        "Stock 1",
        value="RELIANCE.NS"
    ).upper()

with col2:
    stock2 = st.text_input(
        "Stock 2",
        value="TCS.NS"
    ).upper()

# ------------------------
# Compare
# ------------------------

if st.button("🚀 Compare Stocks"):

    with st.spinner("Comparing Stocks..."):

        data1 = compare_stock(stock1)
        data2 = compare_stock(stock2)

    if data1 is None or data2 is None:
        st.error("Unable to fetch one or both stocks.")
        st.stop()

    comparison = pd.DataFrame({
        stock1: data1,
        stock2: data2
    })

    st.subheader("📊 Comparison")

    st.dataframe(
        comparison,
        use_container_width=True
    )

    st.divider()

    # ------------------------
    # Winner
    # ------------------------

    if data1["Score"] > data2["Score"]:

        winner = stock1
        loser = stock2
        win_data = data1
        lose_data = data2

    elif data2["Score"] > data1["Score"]:

        winner = stock2
        loser = stock1
        win_data = data2
        lose_data = data1

    else:

        st.info("🤝 Both stocks have the same overall score.")
        st.stop()

    st.success(f"🏆 Winner : {winner}")

    reasons = []

    if win_data["Fundamental"] > lose_data["Fundamental"]:
        reasons.append("✅ Better Fundamental Score")

    if win_data["Technical"] > lose_data["Technical"]:
        reasons.append("✅ Better Technical Score")

    if win_data["Valuation"] > lose_data["Valuation"]:
        reasons.append("✅ Better Valuation")

    if win_data["Risk"] > lose_data["Risk"]:
        reasons.append("✅ Better Risk Profile")

    st.subheader("💡 Why this stock wins")

    for reason in reasons:
        st.write(reason)

    st.metric(
        "Final Score",
        win_data["Score"]
    )