from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st

from dss.config import DB_CONFIG


def get_engine():
    connection_url = (
        f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return create_engine(connection_url, pool_pre_ping=True)


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
