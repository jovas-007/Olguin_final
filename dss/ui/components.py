import pandas as pd
import streamlit as st


def mostrar_tarjeta_kpi(nombre: str, valor: float, objetivo: float, descripcion: str):
    if pd.isna(valor):
        estado = "Sin datos"
        color = "#ccc"
        valor_str = "N/D"
    else:
        ratio = valor / objetivo if objetivo else 0
        if ratio >= 1.05:
            color = "#2e7d32"
            estado = "Objetivo superado"
        elif ratio >= 0.9:
            color = "#f9a825"
            estado = "Cerca del objetivo"
        else:
            color = "#c62828"
            estado = "Bajo el objetivo"
        valor_str = f"{valor:.2f}"
    objetivo_str = "N/D" if pd.isna(objetivo) else f"{objetivo:.2f}"

    with st.container():
        st.markdown(
            f"""
            <div style='background-color:{color}; padding:12px; border-radius:8px; color:white;'>
                <h4 style='margin:0'>{nombre}</h4>
                <p style='margin:0;'>Valor actual: <b>{valor_str}</b></p>
                <p style='margin:0;'>Objetivo: <b>{objetivo_str}</b></p>
                <p style='margin:0;'>{estado}</p>
                <small>{descripcion}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
