import streamlit as st


def render_price_chart(fig):

    st.divider()

    st.markdown("## 📈 Price Chart")

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "scrollZoom": True,
        },
    )