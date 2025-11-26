from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import streamlit as st

# Ruta a la carpeta de datos
DATA_DIR = Path(__file__).parent.parent / "CargaDatos"


def cargar_datos_desde_csv():
    """Carga todos los archivos CSV y realiza los JOINs necesarios"""
    try:
        # Cargar tablas de hechos
        hechos_proyectos = pd.read_csv(DATA_DIR / "hechos_proyectos_seed.csv")
        hechos_asignaciones = pd.read_csv(DATA_DIR / "hechos_asignaciones_seed.csv")
        
        # Cargar dimensiones
        dim_proyectos = pd.read_csv(DATA_DIR / "dim_proyectos_seed.csv")
        dim_clientes = pd.read_csv(DATA_DIR / "dim_clientes_seed.csv")
        dim_gastos = pd.read_csv(DATA_DIR / "dim_gastos_seed.csv")
        dim_tiempo = pd.read_csv(DATA_DIR / "dim_tiempo_seed.csv")
        dim_empleados = pd.read_csv(DATA_DIR / "dim_empleados_seed.csv")
        
        return {
            "hechos_proyectos": hechos_proyectos,
            "hechos_asignaciones": hechos_asignaciones,
            "dim_proyectos": dim_proyectos,
            "dim_clientes": dim_clientes,
            "dim_gastos": dim_gastos,
            "dim_tiempo": dim_tiempo,
            "dim_empleados": dim_empleados
        }
    except Exception as e:
        st.error(f"Error al cargar archivos CSV: {e}")
        return None


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
    """Carga y une datos de proyectos desde archivos CSV"""
    datos = cargar_datos_desde_csv()
    
    if datos is None:
        return generar_datos_de_ejemplo()[0]
    
    # JOIN: hechos_proyectos + dim_proyectos + dim_clientes + dim_gastos + dim_tiempo
    df = datos["hechos_proyectos"].merge(
        datos["dim_proyectos"], on="ID_Proyecto", how="left"
    ).merge(
        datos["dim_clientes"], on="ID_Cliente", how="left"
    ).merge(
        datos["dim_gastos"], left_on="ID_Gasto", right_on="ID_Finanza", how="left"
    ).merge(
        datos["dim_tiempo"], left_on="ID_FechaInicio", right_on="ID_Tiempo", how="left", suffixes=("", "_inicio")
    ).merge(
        datos["dim_tiempo"], left_on="ID_FechaFin", right_on="ID_Tiempo", how="left", suffixes=("_inicio", "_fin")
    )
    
    # Renombrar columnas para coincidir con el esquema esperado
    df = df.rename(columns={
        "Anio_inicio": "AnioInicio",
        "Mes_inicio": "MesInicio",
        "Anio_fin": "AnioFin",
        "Mes_fin": "MesFin"
    })
    
    # Seleccionar solo las columnas necesarias
    columnas = [
        "ID_Proyecto", "CodigoProyecto", "Version", "Cancelado", "TotalErrores",
        "NumTrabajadores", "CodigoClienteReal", "TipoGasto", "Categoria",
        "Presupuesto", "CosteReal", "DesviacionPresupuestal", "PenalizacionesMonto",
        "ProporcionCAPEX_OPEX", "RetrasoInicioDias", "RetrasoFinalDias",
        "TasaDeErroresEncontrados", "TasaDeExitoEnPruebas", "ProductividadPromedio",
        "PorcentajeTareasRetrasadas", "PorcentajeHitosRetrasados",
        "AnioInicio", "MesInicio", "AnioFin", "MesFin"
    ]
    
    df_result = df[columnas].copy()
    
    # Convertir porcentajes a decimal (0-1) si están en formato 0-100
    for col in ["TasaDeErroresEncontrados", "TasaDeExitoEnPruebas", "PorcentajeTareasRetrasadas", "PorcentajeHitosRetrasados"]:
        if col in df_result.columns:
            # Si los valores son > 1, están en formato 0-100, convertir a 0-1
            if df_result[col].max() > 1:
                df_result[col] = df_result[col] / 100
    
    return df_result


@st.cache_data(show_spinner=False)
def cargar_df_asignaciones() -> pd.DataFrame:
    """Carga y une datos de asignaciones desde archivos CSV"""
    datos = cargar_datos_desde_csv()
    
    if datos is None:
        return generar_datos_de_ejemplo()[1]
    
    # JOIN: hechos_asignaciones + dim_empleados + dim_proyectos + dim_tiempo
    df = datos["hechos_asignaciones"].merge(
        datos["dim_empleados"], on="ID_Empleado", how="left"
    ).merge(
        datos["dim_proyectos"], on="ID_Proyecto", how="left"
    ).merge(
        datos["dim_tiempo"], left_on="ID_FechaAsignacion", right_on="ID_Tiempo", how="left"
    )
    
    # Seleccionar solo las columnas necesarias
    columnas = [
        "ID_Empleado", "CodigoEmpleado", "Rol", "Seniority",
        "ID_Proyecto", "CodigoProyecto", "HorasPlanificadas", "HorasReales",
        "ValorHoras", "RetrasoHoras", "Anio", "Mes"
    ]
    
    return df[columnas]
