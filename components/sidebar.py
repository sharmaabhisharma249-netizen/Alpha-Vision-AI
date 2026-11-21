import streamlit as st
from auth.auth_utils import get_watchlist
from utils.icons import load_svg
from utils.icons import load_svg, sidebar_title
def render_sidebar():

    with st.sidebar:

        icon = load_svg("sidebar", "dashboard", 22)

        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:10px;">
                {icon}
                <h2 style="margin:0;">AlphaVision AI</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("Version 5.0")

        st.divider()

        st.success("🟢 System Online")

        developer_icon = load_svg("sidebar", "developer", 18)

        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:8px;margin-top:15px;">
                {developer_icon}
                <span style="font-size:17px;font-weight:600;">Developer</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("Abhinav Gautam")
        
        brain_icon = load_svg("sidebar", "brain", 18)

        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:8px;margin-top:15px;">
                {brain_icon}
                <span style="font-size:17px;font-weight:600;">AI Model</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("Gemini 2.5 Flash")
        
        modules_icon = load_svg("sidebar", "modules", 18)

        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:8px;margin-top:15px;">
                {modules_icon}
                <span style="font-size:17px;font-weight:600;">Modules</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        modules = [
            "Technical Analysis",
            "Fundamental Analysis",
            "Risk Analysis",
            "Valuation",
            "AI Reports",
            "News Analysis"
        ]

        for module in modules:
            st.write(f"✔ {module}")

        st.divider()

        market_icon = load_svg("sidebar", "market", 18)

        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:8px;margin-top:15px;">
                {market_icon}
                <span style="font-size:17px;font-weight:600;">Market Status</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.info("🟢 Market Data Connected")       

        st.divider()
        if "user" in st.session_state:

            user = st.session_state.user

            st.success(f"👋 Welcome, {user['name']}")

            st.divider()

            watchlist_icon = load_svg("sidebar", "watchlist", 18)

            watchlist_icon = load_svg("sidebar", "watchlist", 18)

            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:8px;margin-top:15px;">
                    {watchlist_icon}
                    <span style="font-size:17px;font-weight:600;">My Watchlist</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            watchlist = get_watchlist(user["id"])

            if not watchlist:

                st.caption("No stocks added yet.")

            else:

                for stock in watchlist:

                    st.write(f"📈 {stock['symbol']}")
        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):
            st.session_state.logged_in = False
            st.session_state.pop("user", None)
            st.rerun()

        st.divider()

        st.caption("Made with ❤️ using Python + Streamlit")