import streamlit as st
from core.market_data import get_dashboard_summary
from datetime import datetime

def render_market_cards():

    summary = get_dashboard_summary()

    indices = summary["indices"]

    with st.container(border=True):

        header_col1, header_col2 = st.columns([5, 1])

        with header_col1:
            st.subheader("📈 Market Indices")

        with header_col2:
            if st.button(
                "🔄 Refresh",
                key="refresh_market",
                use_container_width=True
            ):
                st.cache_data.clear()
                st.rerun()

        cols = st.columns(len(indices))

        for col, (name, data) in zip(cols, indices.items()):

            with col:

                if data["price"] is None:
                    st.metric(
                        label=name,
                        value="N/A",
                        delta="No Data"
                    )
                else:
                    st.metric(
                        label=name,
                        value=f"{data['price']:,.2f}",
                        delta=f"{data['percent']}%"
                    )

        st.markdown("")

        c1, c2 = st.columns(2)

        with c1:
            st.success(f"🤖 AI Mood : {summary['sentiment']['mood']}")

        with c2:
            if summary["market_open"]:
                st.success("🟢 Market Open")
            else:
                st.error("🔴 Market Closed")

        st.caption(
            f"🕒 Last Updated: {datetime.now().strftime('%d %b %Y | %I:%M:%S %p')}"
        )