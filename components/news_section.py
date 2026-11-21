import streamlit as st


def news_card(title, source, time):

    st.markdown(
        f"""
<div class="news-card">

<div class="news-source">
📰 {source}
</div>

<div class="news-title">
{title}
</div>

<div class="news-time">
🕒 {time}
</div>

</div>
""",
        unsafe_allow_html=True,
    )


def render_news():

    st.markdown("## 📰 Latest Market News")

    c1, c2, c3 = st.columns(3)

    with c1:
        news_card(
            "Markets remain volatile ahead of RBI policy meeting.",
            "Economic Times",
            "15 min ago"
        )

    with c2:
        news_card(
            "IT stocks outperform broader market in today's session.",
            "Moneycontrol",
            "28 min ago"
        )

    with c3:
        news_card(
            "Foreign investors increase buying in banking sector.",
            "Business Standard",
            "1 hour ago"
        )