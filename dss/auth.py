import streamlit as st

from dss.config import USERS


def login():
    if "auth" not in st.session_state:
        st.session_state.auth = {"is_authenticated": True, "role": "viewer", "user": "invitado"}

    with st.sidebar.form("login_form"):
        st.subheader("Acceso restringido")
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar sesión")

    if submit:
        user_info = USERS.get(username)
        if user_info and password == user_info["password"]:
            st.session_state.auth = {
                "is_authenticated": True,
                "role": user_info["role"],
                "user": username,
            }
            st.success(f"Bienvenido {username}")
        else:
            st.error("Usuario o contraseña incorrectos")

    if st.session_state.auth["is_authenticated"]:
        st.sidebar.caption(f"Rol: {st.session_state.auth['role']}")
        if st.session_state.auth["user"] != "invitado":
            if st.sidebar.button("Cerrar sesión"):
                st.session_state.auth = {"is_authenticated": True, "role": "viewer", "user": "invitado"}
                st.rerun()
