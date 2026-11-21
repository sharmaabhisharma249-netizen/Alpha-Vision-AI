import streamlit as st


def action_card(icon, title, subtitle):

    st.markdown(
        f"""
<div class="action-card">

<div class="action-icon">
{icon}
</div>

<div class="action-title">
{title}
</div>

<div class="action-subtitle">
{subtitle}
</div>


</div>
""",
        unsafe_allow_html=True,
    )


def render_quick_actions():

    st.markdown("## ⚡ Quick Actions")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        action_card(
            "🔍",
            "Stock Analysis",
            "Technical + AI Insights"
        )

        if st.button(
            "🚀 Open",
            key="stock_analysis",
            use_container_width=True
        ):
            st.switch_page("pages/1_Stock_Analysis.py")

    with c2:
        action_card(
            "📊",
            "AI Screener",
            "Find Best Stocks"
        )

        if st.button(
            "🚀 Open",
            key="screener",
            use_container_width=True
        ):
            st.switch_page("pages/2_Screener.py")

    with c3:
        action_card(
            "⚖️",
            "Compare",
            "Compare Companies"
        )

        if st.button(
            "🚀 Open",
            key="compare",
            use_container_width=True
        ):
            st.switch_page("pages/4_Compare.py")
    with c4:
        action_card(
            "📄",
            "Reports",
            "Export PDF Reports"
        )

        if st.button(
            "🚀 Open",
            key="reports",
            use_container_width=True
        ):
            st.switch_page("pages/5_Reports.py")