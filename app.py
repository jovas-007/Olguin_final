import streamlit as st

from dss.analytics import get_kpis
from dss.auth import login
from dss.data_sources import cargar_df_asignaciones, cargar_df_proyectos
from dss.ui.views import render_detalle, render_prediccion, render_scorecard

st.set_page_config(page_title="DSS – Dashboard de desempeño de proyectos de software", layout="wide")


def main():
    st.title("DSS – Dashboard de desempeño de proyectos de software")
    st.caption(
        "Misión: Optimizar procesos con tecnologa; Visión: decisiones basadas en datos y excelencia sostenible."
    )

    login()

    df_proyectos = cargar_df_proyectos()
    df_asignaciones = cargar_df_asignaciones()

    st.sidebar.header("Filtros analíticos")
    anios = sorted(df_proyectos["AnioFin"].dropna().unique())
    meses = sorted(df_proyectos["MesFin"].dropna().unique())
    clientes = sorted(df_proyectos["CodigoClienteReal"].dropna().unique())
    proyectos = sorted(df_proyectos["CodigoProyecto"].dropna().unique())
    roles = sorted(df_asignaciones["Rol"].dropna().unique())

    filtros = {
        "anio": st.sidebar.multiselect("Año de fin", anios, default=anios),
        "mes": st.sidebar.multiselect("Mes de fin", meses, default=meses),
        "cliente": st.sidebar.multiselect("Cliente", clientes),
        "proyecto": st.sidebar.multiselect("Proyecto", proyectos),
        "rol": st.sidebar.multiselect("Rol/Empleado", roles),
    }

    kpis = get_kpis(df_proyectos, df_asignaciones, filtros)

    tabs = ["Resumen general", "Análisis detallado"]
    if st.session_state.auth.get("role") == "project_manager":
        tabs.append("Predicción de defectos")

    tab_objs = st.tabs(tabs)

    with tab_objs[0]:
        render_scorecard(df_proyectos, df_asignaciones, filtros)
    with tab_objs[1]:
        render_detalle(df_proyectos, df_asignaciones, filtros)

    if "Predicción de defectos" in tabs:
        with tab_objs[2]:
            render_prediccion(df_proyectos, kpis)


if __name__ == "__main__":
    main()
