import streamlit as st


def get_risk_color(level):
    level = str(level).lower()

    if "low" in level:
        return "#22C55E"
    elif "moderate" in level:
        return "#F59E0B"
    return "#EF4444"


def render_risk_panel(risk):

    risk_level = risk.get("riskLevel", "Unknown")
    risk_score = risk.get("score", 0)
    debt = risk.get("debtEquity", "N/A")
    market_cap = risk.get("marketCap", "N/A")

    color = get_risk_color(risk_level)

    st.divider()
    st.markdown("## 🛡️ Risk Analysis")

    c1, c2 = st.columns([2, 1])

    with c1:

        st.markdown(
            f"""
            <div class="score-card-new">

            <h3 style="text-align:center;">Risk Level</h3>

            <h2 style="color:{color}; text-align:center; margin:20px 0;">
                {risk_level}
            </h2>

            <hr>

            <p><b>Debt / Equity :</b> {debt}</p>

            <p><b>Market Cap :</b> {market_cap}</p>

            </div>
              """,
            unsafe_allow_html=True
        )

    with c2:
        st.metric("Risk Score", f"{risk_score}/15")