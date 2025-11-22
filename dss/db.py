from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st

from dss.config import DATABASE_URL


def get_engine():
    # Usar la URL directa con pymysql
    return create_engine(DATABASE_URL, pool_pre_ping=True)


def get_connection():
    try:
        engine = get_engine()
        return engine.connect()
    except SQLAlchemyError as exc:
        st.error(
            "No se pudo conectar a la base de datos. Verifique la configuración y el servicio MySQL."
        )
        st.info(f"Detalle técnico: {exc}")
        return None
