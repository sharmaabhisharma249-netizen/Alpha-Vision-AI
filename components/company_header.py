import streamlit as st


def render_company_header(info):

    st.markdown("## 📈 Company Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Current Price",
        info.get("price", "N/A")
    )

    c2.metric(
        "🏢 Market Cap",
        info.get("marketCap", "N/A")
    )

    c3.metric(
        "📊 P/E Ratio",
        info.get("pe", "N/A")
    )

    c4.metric(
        "📈 52W High",
        info.get("high52", "N/A")
    )

    left, right = st.columns(2)

    with left:

        st.write(f"**Company:** {info.get('name','N/A')}")
        st.write(f"**Sector:** {info.get('sector','N/A')}")
        st.write(f"**Industry:** {info.get('industry','N/A')}")

    with right:

        st.write(f"**52W Low:** {info.get('low52','N/A')}")
        st.write(f"**Volume:** {info.get('volume','N/A')}")