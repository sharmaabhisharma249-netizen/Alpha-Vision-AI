import streamlit as st


def get_color(status):

    status = str(status).lower()

    if "under" in status:
        return "#22C55E"
    elif "fair" in status:
        return "#F59E0B"
    else:
        return "#EF4444"


def render_valuation_panel(valuation):

    valuation_status = valuation.get("valuation", "N/A")
    score = valuation.get("score", 0)

    pe = valuation.get("pe")
    pb = valuation.get("pb")

    pe_text = f"{pe:.2f}" if isinstance(pe, (int, float)) else "N/A"
    pb_text = f"{pb:.2f}" if isinstance(pb, (int, float)) else "N/A"

    color = get_color(valuation_status)

    st.divider()
    st.markdown("## 💰 Valuation Analysis")

    c1, c2 = st.columns([2, 1])

    with c1:

        st.markdown(
            f"""
            <div class="score-card-new">

            <h3>Current Valuation</h3>

            <h2 style="color:{color}">
                {valuation_status}
            </h2>

            <hr>

            <p><b>P/E Ratio :</b> {pe_text}</p>

            <p><b>P/B Ratio :</b> {pb_text}</p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.metric(
            "Valuation Score",
            f"{score}/30"
        )