import json
import os
from pathlib import Path

import streamlit as st


# Ruta del archivo JSON para usuarios registrados
USERS_FILE = Path(__file__).parent.parent / "users.json"


def cargar_usuarios():
    """Carga usuarios desde el archivo JSON"""
    if USERS_FILE.exists():
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def guardar_usuarios(usuarios):
    """Guarda usuarios en el archivo JSON"""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)


def registrar_usuario(username, password):
    """Registra un nuevo usuario con rol project_manager"""
    usuarios = cargar_usuarios()
    
    if username in usuarios:
        return False, "El usuario ya existe"
    
    if len(username) < 3:
        return False, "El usuario debe tener al menos 3 caracteres"
    
    if len(password) < 4:
        return False, "La contraseña debe tener al menos 4 caracteres"
    
    usuarios[username] = {
        "password": password,
        "role": "project_manager"
    }
    
    guardar_usuarios(usuarios)
    return True, "Usuario registrado exitosamente"


def obtener_usuario(username):
    """Obtiene información del usuario desde JSON"""
    usuarios = cargar_usuarios()
    return usuarios.get(username, None)


@st.dialog("Registrar nuevo usuario")
def mostrar_formulario_registro():
    """Muestra ventana emergente para registro"""
    st.write("Crea tu cuenta para acceder al modelo de predicción")
    
    nuevo_usuario = st.text_input("Usuario", key="reg_user")
    nueva_password = st.text_input("Contraseña", type="password", key="reg_pass")
    confirmar_password = st.text_input("Confirmar contraseña", type="password", key="reg_pass_confirm")
    
    if st.button("Registrar", type="primary"):
        if not nuevo_usuario or not nueva_password:
            st.error("Completa todos los campos")
        elif nueva_password != confirmar_password:
            st.error("Las contraseñas no coinciden")
        else:
            exito, mensaje = registrar_usuario(nuevo_usuario, nueva_password)
            if exito:
                st.success(mensaje)
                st.info("Ahora puedes iniciar sesión con tus credenciales")
                st.rerun()
            else:
                st.error(mensaje)


def login():
    if "auth" not in st.session_state:
        st.session_state.auth = {"is_authenticated": True, "role": "viewer", "user": "invitado"}

    with st.sidebar.form("login_form"):
        st.subheader("Acceso restringido")
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar sesión")

    if submit:
        user_info = obtener_usuario(username)
        if user_info and password == user_info["password"]:
            st.session_state.auth = {
                "is_authenticated": True,
                "role": user_info["role"],
                "user": username,
            }
            st.success(f"Bienvenido {username}")
        else:
            st.error("Usuario o contraseña incorrectos")
    
    # Botón de registro debajo del formulario de login
    if st.sidebar.button("📝 Registrar nuevo usuario"):
        mostrar_formulario_registro()

    if st.session_state.auth["is_authenticated"]:
        st.sidebar.caption(f"Rol: {st.session_state.auth['role']}")
        if st.session_state.auth["user"] != "invitado":
            if st.sidebar.button("Cerrar sesión"):
                st.session_state.auth = {"is_authenticated": True, "role": "viewer", "user": "invitado"}
                st.rerun()
