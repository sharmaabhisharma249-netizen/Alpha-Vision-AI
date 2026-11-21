import streamlit as st

import streamlit as st

def score_card(title, score, total, icon, status):

    with st.container(border=True):
        st.markdown(f"## {icon}")
        st.markdown(f"### {title}")
        st.metric("Score", f"{score}/{total}")
        st.write(status)

def render_score_cards(
    technical,
    fundamental,
    valuation,
    risk
):

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        score_card(
            "Technical",
            technical["score"],
            20,
            "📈",
            technical["trend"]
        )

    with c2:
        score_card(
            "Fundamental",
            fundamental["score"],
            70,
            "🏢",
            "Healthy"
        )

    with c3:
        score_card(
            "Valuation",
            valuation["score"],
            30,
            "💰",
            valuation["valuation"]
        )

    with c4:
        score_card(
            "Risk",
            risk["score"],
            15,
            "🛡️",
            risk["riskLevel"]
        )