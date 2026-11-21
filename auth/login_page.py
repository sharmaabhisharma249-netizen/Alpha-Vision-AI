import streamlit as st

from auth.auth_utils import login_user, register_user
from components.hero import render_hero


def render_login():

    # ---------------- HERO ----------------
    render_hero()
   # ---------------- CENTER LOGIN CARD ----------------
    tab1, tab2 = st.tabs(["Login", "Register"])
        # ===================================================
        # LOGIN
        # ===================================================
    with tab1:

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            key="login_btn",
            use_container_width=True
        ):

            success, user = login_user(
                email,
                password
            )

            if success:

                st.session_state.logged_in = True
                st.session_state.user = dict(user)

                st.success(
                    f"Welcome {user['name']} 👋"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Email or Password"
                )

        # ===================================================
        # REGISTER
        # ===================================================
    with tab2:

        name = st.text_input(
            "Full Name",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            key="register_email"
        )

        password = st.text_input(
            "Password",
            type="password",
               key="register_password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm"
        )

        if st.button(
            "Create Account",
            key="register_btn",
            use_container_width=True
        ):

            if password != confirm:

                st.error(
                    "Passwords do not match."
                )

            else:

                ok, message = register_user(
                    name,
                    email,
                    password
                )

                if ok:

                    st.success(message)

                else:

                    st.error(message)
                        