from core.data_fetcher import get_stock_info
from components.hero import render_hero
from components.sidebar import render_sidebar
from components.market_cards import render_market_cards
from components.market_cards import render_market_cards
from components.quick_actions import render_quick_actions
from components.news_section import render_news
from components.sidebar import render_sidebar
from auth.database import (
    create_users_table,
    create_watchlist_table
)
from auth.login_page import render_login
from auth.database import create_users_table
from core.nse_stocks import load_nse_stocks
stocks = load_nse_stocks()

print(stocks.head())
print(stocks.shape)
import streamlit as st
create_users_table()
create_users_table()
create_watchlist_table()


st.set_page_config(
    page_title="AlphaVision AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.logged_in:
    render_login()
    st.stop()
    
render_sidebar()

render_hero()

render_market_cards()

render_quick_actions()

render_news()

st.markdown("""
<div class="card">

<h2 style="margin-top:0;">
🔍 Search Any NSE Stock
</h2>

<p style="color:#94A3B8;">
Analyze any Indian stock using AI in seconds.
</p>

</div>
""", unsafe_allow_html=True)
st.markdown("## 🔍 Stock Search")

stock = st.text_input(

    "",

    placeholder="Search NSE Stock (Example: RELIANCE.NS)"

)
analyze = st.button(
    "🚀 Analyze Stock",
    use_container_width=True
)

# Welcome Screen
if not stock:
    st.info("👆 Enter a stock symbol to begin.")
    st.stop()

# Analysis
if analyze:

    with st.spinner("Fetching market data..."):
        info = get_stock_info(stock)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💵 Price", info.get("price"))
    c2.metric("🏢 Market Cap", info.get("marketCap"))
    c3.metric("📊 PE", info.get("pe"))
    c4.metric("📈 52W High", info.get("high52"))

    st.divider()

    st.subheader("🏢 Company Overview")

    l, r = st.columns(2)

    with l:
        st.write(f"**Company:** {info.get('name')}")
        st.write(f"**Current Price:** {info.get('price')}")
        st.write(f"**P/E:** {info.get('pe')}")

    with r:
        st.write(f"**52W High:** {info.get('high52')}")
        st.write(f"**52W Low:** {info.get('low52')}")
        st.write(f"**Volume:** {info.get('volume')}")

        st.info("Continue integrating your existing chart, analysis, AI, reports and news sections below this point.")

st.markdown("---")
st.caption("AlphaVision AI • Powered by Streamlit + Gemini")
