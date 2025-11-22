import os
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import rayleigh
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

st.set_page_config(page_title="DSS – Dashboard de desempeño de proyectos de software", layout="wide")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3307)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", " "),
    "database": os.getenv("DB_NAME", "dw_proyectos"),
}

USERS = {
    "pm1": {"password": "1234", "role": "project_manager"},
    "analista1": {"password": "abcd", "role": "viewer"},
}

KPI_TARGETS = {
    "cumplimiento_presupuesto": 0.9,
    "desviacion_presupuestal": 0.05,
    "penalizaciones_sobre_presupuesto": 0.02,
    "proyectos_a_tiempo": 0.85,
    "proyectos_cancelados": 0.05,
    "porcentaje_tareas_retrasadas": 0.1,
    "porcentaje_hitos_retrasados": 0.1,
    "tasa_errores": 0.05,
    "productividad_promedio": 0.75,
    "tasa_exito_pruebas": 0.9,
    "horas_relacion": 1.1,
}


# ---------------------------------------------------------------------------
# Conexión y carga de datos
# ---------------------------------------------------------------------------

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


@st.cache_data(show_spinner=False)
def cargar_df_proyectos() -> pd.DataFrame:
    conn = get_connection()
    if conn is None:
        return generar_datos_de_ejemplo()[0]

    query = text(
        """
        SELECT
            hp.ID_Proyecto,
            dp.CodigoProyecto,
            dp.Version,
            dp.Cancelado,
            dp.TotalErrores,
            dp.NumTrabajadores,
            dc.CodigoClienteReal,
            gi.TipoGasto,
            gi.Categoria,
            hp.Presupuesto,
            hp.CosteReal,
            hp.DesviacionPresupuestal,
            hp.PenalizacionesMonto,
            hp.ProporcionCAPEX_OPEX,
            hp.RetrasoInicioDias,
            hp.RetrasoFinalDias,
            hp.TasaDeErroresEncontrados,
            hp.TasaDeExitoEnPruebas,
            hp.ProductividadPromedio,
            hp.PorcentajeTareasRetrasadas,
            hp.PorcentajeHitosRetrasados,
            ti_inicio.Anio AS AnioInicio,
            ti_inicio.Mes AS MesInicio,
            ti_fin.Anio AS AnioFin,
            ti_fin.Mes AS MesFin
        FROM hechos_proyectos hp
        JOIN dim_proyectos dp ON hp.ID_Proyecto = dp.ID_Proyecto
        JOIN dim_clientes dc ON dp.ID_Cliente = dc.ID_Cliente
        JOIN dim_gastos gi ON hp.ID_Gasto = gi.ID_Finanza
        JOIN dim_tiempo ti_inicio ON hp.ID_FechaInicio = ti_inicio.ID_Tiempo
        JOIN dim_tiempo ti_fin ON hp.ID_FechaFin = ti_fin.ID_Tiempo
        """
    )
    try:
        df = pd.read_sql(query, conn)
    except SQLAlchemyError as exc:
        st.error("Error al consultar hechos_proyectos. Usando datos de ejemplo.")
        st.info(f"Detalle técnico: {exc}")
        df = generar_datos_de_ejemplo()[0]
    finally:
        conn.close()
    return df


@st.cache_data(show_spinner=False)
def cargar_df_asignaciones() -> pd.DataFrame:
    conn = get_connection()
    if conn is None:
        return generar_datos_de_ejemplo()[1]

    query = text(
        """
        SELECT
            ha.ID_Empleado,
            de.CodigoEmpleado,
            de.Rol,
            de.Seniority,
            ha.ID_Proyecto,
            dp.CodigoProyecto,
            ha.HorasPlanificadas,
            ha.HorasReales,
            ha.ValorHoras,
            ha.RetrasoHoras,
            dt.Anio,
            dt.Mes
        FROM hechos_asignaciones ha
        JOIN dim_empleados de ON ha.ID_Empleado = de.ID_Empleado
        JOIN dim_proyectos dp ON ha.ID_Proyecto = dp.ID_Proyecto
        JOIN dim_tiempo dt ON ha.ID_FechaAsignacion = dt.ID_Tiempo
        """
    )
    try:
        df = pd.read_sql(query, conn)
    except SQLAlchemyError as exc:
        st.error("Error al consultar hechos_asignaciones. Usando datos de ejemplo.")
        st.info(f"Detalle técnico: {exc}")
        df = generar_datos_de_ejemplo()[1]
    finally:
        conn.close()
    return df


def generar_datos_de_ejemplo() -> Tuple[pd.DataFrame, pd.DataFrame]:
    np.random.seed(42)
    proyectos = pd.DataFrame(
        {
            "ID_Proyecto": [1, 2, 3, 4],
            "CodigoProyecto": [1001, 1002, 1003, 1004],
            "Version": [1, 1, 2, 1],
            "Cancelado": [0, 0, 1, 0],
            "TotalErrores": [120, 80, 200, 150],
            "NumTrabajadores": [10, 8, 12, 9],
            "CodigoClienteReal": [501, 502, 503, 501],
            "TipoGasto": ["Licencias", "Viajes", "Servicios", "Capacitacion"],
            "Categoria": ["CAPEX", "OPEX", "OPEX", "CAPEX"],
            "Presupuesto": [500000, 300000, 450000, 350000],
            "CosteReal": [520000, 280000, 500000, 340000],
            "DesviacionPresupuestal": [20000, -20000, 50000, -10000],
            "PenalizacionesMonto": [5000, 0, 20000, 0],
            "ProporcionCAPEX_OPEX": [0.6, 0.4, 0.7, 0.5],
            "RetrasoInicioDias": [5, -2, 0, 3],
            "RetrasoFinalDias": [10, 0, 15, -1],
            "TasaDeErroresEncontrados": [0.07, 0.05, 0.1, 0.06],
            "TasaDeExitoEnPruebas": [0.9, 0.95, 0.85, 0.92],
            "ProductividadPromedio": [0.78, 0.82, 0.7, 0.8],
            "PorcentajeTareasRetrasadas": [0.12, 0.08, 0.2, 0.1],
            "PorcentajeHitosRetrasados": [0.1, 0.07, 0.15, 0.09],
            "AnioInicio": [2023, 2023, 2024, 2024],
            "MesInicio": [1, 4, 2, 6],
            "AnioFin": [2023, 2023, 2024, 2024],
            "MesFin": [6, 8, 10, 11],
        }
    )

    asignaciones = pd.DataFrame(
        {
            "ID_Empleado": [1, 2, 3, 1, 2, 3],
            "CodigoEmpleado": [2001, 2002, 2003, 2001, 2002, 2003],
            "Rol": ["Developer", "QA", "PM", "Developer", "QA", "PM"],
            "Seniority": ["Semi", "Senior", "Senior", "Semi", "Senior", "Senior"],
            "ID_Proyecto": [1, 1, 1, 2, 2, 3],
            "CodigoProyecto": [1001, 1001, 1001, 1002, 1002, 1003],
            "HorasPlanificadas": [400, 200, 150, 350, 180, 250],
            "HorasReales": [420, 210, 170, 300, 170, 280],
            "ValorHoras": [35, 40, 60, 35, 40, 60],
            "RetrasoHoras": [10, 5, 8, -20, -5, 15],
            "Anio": [2023, 2023, 2023, 2023, 2023, 2024],
            "Mes": [1, 2, 3, 4, 5, 6],
        }
    )
    return proyectos, asignaciones


# ---------------------------------------------------------------------------
# Capa analítica tipo cubo OLAP
# ---------------------------------------------------------------------------

def aplicar_filtros(df: pd.DataFrame, filtros: Dict) -> pd.DataFrame:
    filtrado = df.copy()
    if filtros.get("anio"):
        filtrado = filtrado[filtrado["AnioFin"].isin(filtros["anio"])]
    if filtros.get("mes"):
        filtrado = filtrado[filtrado["MesFin"].isin(filtros["mes"])]
    if filtros.get("cliente"):
        filtrado = filtrado[filtrado["CodigoClienteReal"].isin(filtros["cliente"])]
    if filtros.get("proyecto"):
        filtrado = filtrado[filtrado["CodigoProyecto"].isin(filtros["proyecto"])]
    return filtrado


def aplicar_filtros_asignaciones(df: pd.DataFrame, filtros: Dict) -> pd.DataFrame:
    filtrado = df.copy()
    if filtros.get("anio"):
        filtrado = filtrado[filtrado["Anio"].isin(filtros["anio"])]
    if filtros.get("mes"):
        filtrado = filtrado[filtrado["Mes"].isin(filtros["mes"])]
    if filtros.get("proyecto"):
        filtrado = filtrado[filtrado["CodigoProyecto"].isin(filtros["proyecto"])]
    if filtros.get("rol"):
        filtrado = filtrado[filtrado["Rol"].isin(filtros["rol"])]
    return filtrado


def get_kpis(df_proy: pd.DataFrame, df_asig: pd.DataFrame, filtros: Dict) -> Dict:
    proyectos = aplicar_filtros(df_proy, filtros)
    asignaciones = aplicar_filtros_asignaciones(df_asig, filtros)

    cumplimiento = 1 - (proyectos["CosteReal"] - proyectos["Presupuesto"]) / proyectos["Presupuesto"]
    penalizaciones = proyectos["PenalizacionesMonto"] / proyectos["Presupuesto"]
    proyectos_a_tiempo = (proyectos["RetrasoFinalDias"] <= 0).mean() if not proyectos.empty else 0
    proyectos_cancelados = (proyectos["Cancelado"] == 1).mean() if not proyectos.empty else 0
    horas_relacion = (
        asignaciones["HorasReales"].sum() / asignaciones["HorasPlanificadas"].sum()
        if asignaciones["HorasPlanificadas"].sum() > 0
        else np.nan
    )

    return {
        "cumplimiento_presupuesto": cumplimiento.mean() if not proyectos.empty else np.nan,
        "desviacion_presupuestal": proyectos["DesviacionPresupuestal"].mean() if not proyectos.empty else np.nan,
        "penalizaciones_sobre_presupuesto": penalizaciones.mean() if not proyectos.empty else np.nan,
        "proyectos_a_tiempo": proyectos_a_tiempo,
        "proyectos_cancelados": proyectos_cancelados,
        "porcentaje_tareas_retrasadas": proyectos["PorcentajeTareasRetrasadas"].mean()
        if not proyectos.empty
        else np.nan,
        "porcentaje_hitos_retrasados": proyectos["PorcentajeHitosRetrasados"].mean()
        if not proyectos.empty
        else np.nan,
        "tasa_errores": proyectos["TasaDeErroresEncontrados"].mean() if not proyectos.empty else np.nan,
        "productividad_promedio": proyectos["ProductividadPromedio"].mean() if not proyectos.empty else np.nan,
        "tasa_exito_pruebas": proyectos["TasaDeExitoEnPruebas"].mean() if not proyectos.empty else np.nan,
        "horas_relacion": horas_relacion,
    }


def get_detail_table(df_proy: pd.DataFrame, filtros: Dict) -> pd.DataFrame:
    proyectos = aplicar_filtros(df_proy, filtros)
    columnas = [
        "CodigoClienteReal",
        "CodigoProyecto",
        "Presupuesto",
        "CosteReal",
        "DesviacionPresupuestal",
        "RetrasoInicioDias",
        "RetrasoFinalDias",
        "ProductividadPromedio",
        "PorcentajeTareasRetrasadas",
        "PorcentajeHitosRetrasados",
    ]
    return proyectos[columnas]


def build_olap_views(df_proyectos: pd.DataFrame, df_asignaciones: pd.DataFrame, filtros: Dict):
    proyectos = aplicar_filtros(df_proyectos, filtros)
    asignaciones = aplicar_filtros_asignaciones(df_asignaciones, filtros)

    barras_presupuesto = proyectos[["CodigoProyecto", "Presupuesto", "CosteReal"]]

    if not proyectos.empty:
        proyectos["FechaFin"] = pd.to_datetime(
            proyectos[["AnioFin", "MesFin"]].assign(Dia=1)
        )
        proyectos_a_tiempo = (
            proyectos.assign(A_Tiempo=(proyectos["RetrasoFinalDias"] <= 0).astype(int))
            .groupby(proyectos["FechaFin"].dt.to_period("M"))["A_Tiempo"]
            .mean()
            .reset_index()
        )
        proyectos_a_tiempo["Fecha"] = proyectos_a_tiempo["FechaFin"].dt.to_timestamp()
    else:
        proyectos_a_tiempo = pd.DataFrame(columns=["Fecha", "A_Tiempo"])

    capex_opex = (
        proyectos.groupby(["Categoria"])["ProporcionCAPEX_OPEX"].mean().reset_index()
        if not proyectos.empty
        else pd.DataFrame(columns=["Categoria", "ProporcionCAPEX_OPEX"])
    )

    retrasos = proyectos[["CodigoProyecto", "RetrasoInicioDias", "RetrasoFinalDias"]]
    productividad_por_rol = (
        asignaciones.groupby("Rol")[["HorasReales", "HorasPlanificadas"]]
        .sum()
        .reset_index()
        if not asignaciones.empty
        else pd.DataFrame(columns=["Rol", "HorasReales", "HorasPlanificadas"])
    )

    return {
        "barras_presupuesto": barras_presupuesto,
        "proyectos_a_tiempo": proyectos_a_tiempo,
        "capex_opex": capex_opex,
        "retrasos": retrasos,
        "productividad_por_rol": productividad_por_rol,
        "asignaciones": asignaciones,
    }


# ---------------------------------------------------------------------------
# Módulo de predicción de defectos
# ---------------------------------------------------------------------------

def preparar_features_target(df: pd.DataFrame):
    features = df[
        [
            "Presupuesto",
            "NumTrabajadores",
            "RetrasoInicioDias",
            "RetrasoFinalDias",
            "ProductividadPromedio",
        ]
    ]
    target = df["TotalErrores"]
    return features, target


@st.cache_data(show_spinner=False)
def entrenar_modelo(df_proyectos: pd.DataFrame) -> LinearRegression:
    features, target = preparar_features_target(df_proyectos)
    modelo = LinearRegression()
    modelo.fit(features, target)
    return modelo


def rayleigh_curve(total_defectos: float, duracion: int, sigma: float) -> pd.DataFrame:
    tiempo = np.linspace(0, duracion, num=duracion + 1)
    cdf = rayleigh.cdf(tiempo, scale=sigma)
    defectos_acumulados = total_defectos * cdf
    return pd.DataFrame({"Tiempo": tiempo, "DefectosAcumulados": defectos_acumulados})


def calcular_sigma(duracion: int, complejidad: str) -> float:
    base = max(duracion / 4, 1)
    factor = {"baja": 0.8, "media": 1.0, "alta": 1.3}.get(complejidad, 1.0)
    return base * factor


# ---------------------------------------------------------------------------
# UI y utilidades
# ---------------------------------------------------------------------------

def mostrar_tarjeta_kpi(nombre: str, valor: float, objetivo: float, descripcion: str):
    if pd.isna(valor):
        estado = "⚠️ Sin datos"
        color = "#ccc"
        valor_str = "N/D"
    else:
        ratio = valor / objetivo if objetivo else 0
        if ratio >= 1.05:
            color = "#2e7d32"
            estado = "✅ Objetivo superado"
        elif ratio >= 0.9:
            color = "#f9a825"
            estado = "🟡 Cerca del objetivo"
        else:
            color = "#c62828"
            estado = "🔴 Bajo el objetivo"
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


def login():
    if "auth" not in st.session_state:
        st.session_state.auth = {"is_authenticated": False, "role": None, "user": None}

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
        if st.sidebar.button("Cerrar sesión"):
            st.session_state.auth = {"is_authenticated": False, "role": None, "user": None}
            st.experimental_rerun()


# ---------------------------------------------------------------------------
# Aplicación principal
# ---------------------------------------------------------------------------

def main():
    st.title("DSS – Dashboard de desempeño de proyectos de software")
    st.caption(
        "Misión: Optimizar procesos con tecnología; Visión: decisiones basadas en datos y excelencia sostenible."
    )

    login()

    df_proyectos = cargar_df_proyectos()
    df_asignaciones = cargar_df_asignaciones()

    # Filtros
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
    vistas = build_olap_views(df_proyectos, df_asignaciones, filtros)
    detalle = get_detail_table(df_proyectos, filtros)

    tabs = ["Resumen general", "Análisis detallado"]
    if st.session_state.auth.get("role") == "project_manager":
        tabs.append("Predicción de defectos")

    tab_objs = st.tabs(tabs)

    with tab_objs[0]:
        st.header("Balanced Scorecard / Cuadro de Mando Integral")
        col_fin, col_cli = st.columns(2)
        with col_fin:
            st.subheader("Perspectiva financiera")
            mostrar_tarjeta_kpi(
                "Cumplimiento de presupuesto",
                kpis["cumplimiento_presupuesto"],
                KPI_TARGETS["cumplimiento_presupuesto"],
                "Refleja eficiencia financiera alineada a sostenibilidad y optimización.",
            )
            mostrar_tarjeta_kpi(
                "Desviación presupuestal promedio",
                kpis["desviacion_presupuestal"],
                KPI_TARGETS["desviacion_presupuestal"],
                "Control estricto de costos para mantener rentabilidad y resiliencia.",
            )
            mostrar_tarjeta_kpi(
                "Penalizaciones sobre presupuesto",
                kpis["penalizaciones_sobre_presupuesto"],
                KPI_TARGETS["penalizaciones_sobre_presupuesto"],
                "Minimiza riesgos económicos y refuerza acuerdos de calidad.",
            )
        with col_cli:
            st.subheader("Perspectiva del cliente")
            mostrar_tarjeta_kpi(
                "Proyectos entregados a tiempo",
                kpis["proyectos_a_tiempo"],
                KPI_TARGETS["proyectos_a_tiempo"],
                "Cumplimiento de compromisos aumenta confianza y fidelidad.",
            )
            mostrar_tarjeta_kpi(
                "Proyectos cancelados",
                1 - kpis["proyectos_cancelados"],
                1 - KPI_TARGETS["proyectos_cancelados"],
                "Gestión de riesgos temprana evita cancelaciones y refuerza la reputación.",
            )

        col_proc, col_learning = st.columns(2)
        with col_proc:
            st.subheader("Perspectiva de procesos internos")
            mostrar_tarjeta_kpi(
                "Porcentaje de tareas retrasadas",
                1 - kpis["porcentaje_tareas_retrasadas"],
                1 - KPI_TARGETS["porcentaje_tareas_retrasadas"],
                "Menos retrasos implica operación ágil y trazable.",
            )
            mostrar_tarjeta_kpi(
                "Porcentaje de hitos retrasados",
                1 - kpis["porcentaje_hitos_retrasados"],
                1 - KPI_TARGETS["porcentaje_hitos_retrasados"],
                "Entrega disciplinada de hitos acelera valor al cliente.",
            )
            mostrar_tarjeta_kpi(
                "Tasa de errores encontrados",
                1 - kpis["tasa_errores"],
                1 - KPI_TARGETS["tasa_errores"],
                "Calidad del producto mejora satisfacción y reduce reprocesos.",
            )
        with col_learning:
            st.subheader("Perspectiva de aprendizaje e innovación")
            mostrar_tarjeta_kpi(
                "Productividad promedio",
                kpis["productividad_promedio"],
                KPI_TARGETS["productividad_promedio"],
                "Colaboración interdisciplinaria y mejora continua.",
            )
            mostrar_tarjeta_kpi(
                "Tasa de éxito en pruebas",
                kpis["tasa_exito_pruebas"],
                KPI_TARGETS["tasa_exito_pruebas"],
                "Pruebas efectivas aseguran software confiable e innovador.",
            )
            mostrar_tarjeta_kpi(
                "Relación horas reales / planificadas",
                kpis["horas_relacion"],
                KPI_TARGETS["horas_relacion"],
                "Planificación precisa favorece proyectos medibles y escalables.",
            )

        st.subheader("Visualizaciones clave")
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(
                vistas["barras_presupuesto"].set_index("CodigoProyecto")[["Presupuesto", "CosteReal"]],
                use_container_width=True,
            )
            st.caption("Comparación Presupuesto vs Coste Real por proyecto para vigilar eficiencia financiera.")
        with col2:
            if not vistas["proyectos_a_tiempo"].empty:
                st.line_chart(
                    vistas["proyectos_a_tiempo"].set_index("Fecha")[["A_Tiempo"]],
                    use_container_width=True,
                )
            else:
                st.info("Sin datos suficientes para evolución mensual de entregas a tiempo.")
            st.caption("Evolución mensual de proyectos entregados a tiempo: apoya decisiones preventivas.")

        st.bar_chart(
            vistas["capex_opex"].set_index("Categoria")[["ProporcionCAPEX_OPEX"]],
            use_container_width=True,
        )
        st.caption("Distribución CAPEX/OPEX promedio por categoría de gasto para equilibrar inversiones.")

    with tab_objs[1]:
        st.header("Análisis detallado")
        st.dataframe(detalle, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Distribución de retrasos por proyecto")
            st.bar_chart(
                vistas["retrasos"].set_index("CodigoProyecto")[["RetrasoInicioDias", "RetrasoFinalDias"]],
                use_container_width=True,
            )
            st.caption("Identifica proyectos críticos y ayuda a replanificar recursos.")
        with col_b:
            st.subheader("Productividad por rol")
            if not vistas["productividad_por_rol"].empty:
                data = vistas["productividad_por_rol"]
                data["Relacion"] = data["HorasReales"] / data["HorasPlanificadas"]
                st.bar_chart(data.set_index("Rol")["Relacion"], use_container_width=True)
            else:
                st.info("Sin datos de asignaciones para el filtro actual.")
            st.caption("Visibiliza eficiencia por rol/empleado para promover coaching y balance de cargas.")

        st.subheader("Horas planificadas vs reales")
        if not vistas["asignaciones"].empty:
            pivot = vistas["asignaciones"].pivot_table(
                index="CodigoProyecto",
                values=["HorasPlanificadas", "HorasReales"],
                aggfunc="sum",
            )
            st.bar_chart(pivot, use_container_width=True)
        else:
            st.info("No hay asignaciones para mostrar en el rango seleccionado.")
        st.caption("Analiza desviaciones operativas para ajustar estimaciones futuras.")

    if "Predicción de defectos" in tabs:
        with tab_objs[2]:
            st.header("Predicción de defectos (Distribución de Rayleigh)")
            st.write(
                "Estimación de defectos para planear pruebas e inspecciones basadas en historial y curva Rayleigh."
            )

            modelo = entrenar_modelo(df_proyectos)

            with st.form("prediccion_form"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    presupuesto = st.number_input("Presupuesto estimado", value=400000.0, step=5000.0)
                    duracion = st.slider("Duración estimada (semanas)", 4, 52, 16)
                with col2:
                    trabajadores = st.number_input("Tamaño de equipo", value=8, step=1)
                    retraso_inicio = st.number_input("Retraso inicial esperado (días)", value=0)
                with col3:
                    retraso_final = st.number_input("Retraso final esperado (días)", value=0)
                    complejidad = st.selectbox("Complejidad", ["baja", "media", "alta"], index=1)
                submitted = st.form_submit_button("Calcular predicción")

            if submitted:
                features = pd.DataFrame(
                    [
                        {
                            "Presupuesto": presupuesto,
                            "NumTrabajadores": trabajadores,
                            "RetrasoInicioDias": retraso_inicio,
                            "RetrasoFinalDias": retraso_final,
                            "ProductividadPromedio": kpis["productividad_promedio"] or 0.75,
                        }
                    ]
                )
                pred_defectos = float(modelo.predict(features)[0])
                sigma = calcular_sigma(duracion, complejidad)
                curva = rayleigh_curve(pred_defectos, duracion, sigma)

                st.metric("Defectos totales esperados", f"{pred_defectos:,.0f}")
                st.line_chart(curva.set_index("Tiempo"), use_container_width=True)
                st.dataframe(curva.head(10))
                st.info(
                    "La curva Rayleigh muestra cómo se acumulan los defectos detectados en el tiempo. "
                    "Planifica más pruebas al inicio si la pendiente es alta o redistribuye esfuerzo cuando se aplane."
                )

            if st.button("Reentrenar modelo"):
                entrenar_modelo.clear()
                st.success("Modelo reentrenado con los datos actuales.")


if __name__ == "__main__":
    main()
