import streamlit as st

from dss.analytics import get_kpis
from dss.auth import login
from dss.data_sources import cargar_df_asignaciones, cargar_df_proyectos
from dss.ui.views import render_detalle, render_prediccion, render_scorecard, render_metricas_calculadas, render_okrs, render_analisis_visual

st.set_page_config(page_title="DSS: Decision Support System", layout="wide")


def main():
    # CSS para centrar los tabs
    st.markdown("""
        <style>
        .stTabs [data-baseweb="tab-list"] {
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("DSS: Decision Support System")
    st.caption(
        "Misión: Optimizar procesos con tecnología | Visión: Decisiones basadas en datos y excelencia sostenible"
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

    # Tabs principales: Balanced Scorecard, Dashboard y Modelo de Predicción (para admin)
    main_tab_names = [" Balanced Scorecard", " Dashboard"]
    if st.session_state.auth.get("role") == "project_manager":
        main_tab_names.append(" Modelo de Predicción")
    
    main_tabs = st.tabs(main_tab_names)
    
    # ============= TAB 1: BALANCED SCORECARD =============
    with main_tabs[0]:
        # Sub-tabs dentro de Balanced Scorecard
        bsc_tabs = st.tabs(["MAIN", "OKRs"])
        
        with bsc_tabs[0]:
            render_scorecard(df_proyectos, df_asignaciones, filtros)
        with bsc_tabs[1]:
            render_okrs(df_proyectos, df_asignaciones, filtros)
    
    # ============= TAB 2: DASHBOARD =============
    with main_tabs[1]:
        # Sub-tabs dentro de Dashboard
        dashboard_tabs = st.tabs(["Análisis Visual", "Análisis Detallado", "Métricas Calculadas"])
        
        with dashboard_tabs[0]:
            render_analisis_visual(df_proyectos, df_asignaciones, filtros)
        with dashboard_tabs[1]:
            render_detalle(df_proyectos, df_asignaciones, filtros)
        with dashboard_tabs[2]:
            render_metricas_calculadas(filtros)
    
    # ============= TAB 3: MODELO DE PREDICCIÓN (solo para admin) =============
    if st.session_state.auth.get("role") == "project_manager":
        with main_tabs[2]:
            render_prediccion(df_proyectos, kpis)


if __name__ == "__main__":
    main()
