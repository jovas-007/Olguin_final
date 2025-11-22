from typing import Tuple

import numpy as np
import pandas as pd
import streamlit as st
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from dss.db import get_connection


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
