import streamlit as st


def get_color(recommendation):

    recommendation = recommendation.upper()

    if recommendation == "BUY":
        return "#22C55E"

    elif recommendation == "HOLD":
        return "#F59E0B"

    return "#EF4444"


def calculate_confidence(score):

    confidence = min(round((score / 140) * 100), 99)

    return confidence


def render_ai_recommendation(
        recommendation,
        score,
        technical,
        fundamental,
        risk,
        sentiment
):

    confidence = calculate_confidence(score)

    color = get_color(recommendation)

    st.divider()

    st.markdown("## 🤖 AlphaVision AI Recommendation")

    st.markdown(
        f"""
        <div class="score-card-new">

        <h1 style="color:{color};">
        {recommendation}
        </h1>

        <hr>

        <h3>Confidence : {confidence}%</h3>

        <br>

        <p>✔ Technical : {technical['trend']}</p>

        <p>✔ Fundamental Score : {fundamental['score']}/70</p>

        <p>✔ Risk : {risk['riskLevel']}</p>

        <p>✔ News Sentiment : {sentiment}</p>

        <hr>

        <h3>Overall Score : {score}/140</h3>

        </div>
        """,
        unsafe_allow_html=True
    )