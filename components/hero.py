import streamlit as st


def render_hero():
    col1, col2, col3 =  st.columns([1.3,1,0.7])
    
    with col2:
        st.image(
            "assets/logo_icon.png",
            width=180
        )
    
    st.markdown(
        """
        <div class="hero-section">
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h1 class="hero-title">
            AlphaVision AI
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="hero-subtitle">
            AI-Powered Investment Intelligence Platform
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="hero-tagline">
            From Analysis to Action — Powered by AI
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True
    )