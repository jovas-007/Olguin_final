"""
Módulo para calcular métricas dinámicamente según especificaciones del proyecto.
Complementa los datos precalculados con cálculos en tiempo real.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).parent.parent / "CargaDatos"


@st.cache_data(show_spinner=False)
def cargar_tablas_completas():
    """Carga todas las tablas necesarias para cálculos de métricas"""
    return {
        "hechos_proyectos": pd.read_csv(DATA_DIR / "hechos_proyectos_seed.csv"),
        "hechos_asignaciones": pd.read_csv(DATA_DIR / "hechos_asignaciones_seed.csv"),
        "dim_proyectos": pd.read_csv(DATA_DIR / "dim_proyectos_seed.csv"),
        "dim_clientes": pd.read_csv(DATA_DIR / "dim_clientes_seed.csv"),
        "dim_gastos": pd.read_csv(DATA_DIR / "dim_gastos_seed.csv"),
        "dim_tiempo": pd.read_csv(DATA_DIR / "dim_tiempo_seed.csv"),
        "dim_empleados": pd.read_csv(DATA_DIR / "dim_empleados_seed.csv"),
        "dim_hitos": pd.read_csv(DATA_DIR / "dim_hitos_seed.csv"),
        "dim_tareas": pd.read_csv(DATA_DIR / "dim_tareas_seed.csv"),
        "dim_pruebas": pd.read_csv(DATA_DIR / "dim_pruebas_seed.csv"),
    }


def calcular_duracion_real_dias(id_proyecto: int, tablas: dict) -> int:
    """
    Métrica: DuracionRealDias
    Fórmula: FechaFinalizacionReal - FechaInicio
    """
    hp = tablas["hechos_proyectos"]
    dt = tablas["dim_tiempo"]
    
    proyecto = hp[hp["ID_Proyecto"] == id_proyecto].iloc[0]
    
    fecha_inicio = dt[dt["ID_Tiempo"] == proyecto["ID_FechaInicio"]].iloc[0]
    fecha_fin = dt[dt["ID_Tiempo"] == proyecto["ID_FechaFin"]].iloc[0]
    
    fecha_inicio_dt = pd.to_datetime(f"{fecha_inicio['Anio']}-{fecha_inicio['Mes']}-{fecha_inicio['Dia']}")
    fecha_fin_dt = pd.to_datetime(f"{fecha_fin['Anio']}-{fecha_fin['Mes']}-{fecha_fin['Dia']}")
    
    return (fecha_fin_dt - fecha_inicio_dt).days


def calcular_numero_defectos_encontrados(id_proyecto: int, tablas: dict) -> int:
    """
    Métrica: NumeroDefectosEncontrados
    Fórmula: COUNT(ID_Prueba WHERE PruebaExitosa = 0)
    Fuente: dim_pruebas, sistema de control de calidad
    """
    hitos_proyecto = tablas["dim_hitos"][
        tablas["dim_hitos"]["ID_proyectos"] == id_proyecto
    ]["ID_Hito"].values
    
    pruebas_proyecto = tablas["dim_pruebas"][
        tablas["dim_pruebas"]["ID_Hito"].isin(hitos_proyecto)
    ]
    
    # Contar pruebas fallidas (defectos encontrados)
    defectos = (pruebas_proyecto["PruebaExitosa"] == 0).sum()
    
    return int(defectos)


def calcular_productividad_promedio(id_proyecto: int, tablas: dict) -> float:
    """
    Métrica: ProductividadPromedio
    Fórmula: DuracionReal / No_empleados
    Fuente: hechos_asignaciones, dim_tareas
    """
    duracion_dias = calcular_duracion_real_dias(id_proyecto, tablas)
    num_empleados = tablas["dim_proyectos"][
        tablas["dim_proyectos"]["ID_Proyecto"] == id_proyecto
    ]["NumTrabajadores"].iloc[0]
    
    if num_empleados > 0:
        return duracion_dias / num_empleados
    return 0.0


def calcular_porcentaje_tareas_retrasadas(id_proyecto: int, tablas: dict) -> float:
    """
    Métrica: PorcentajeTareasRetrasadas
    Fórmula: (COUNT(TareasRetrasadas) / COUNT(TareasTotales)) × 100
    Fuente: dim_tareas
    """
    hitos_proyecto = tablas["dim_hitos"][
        tablas["dim_hitos"]["ID_proyectos"] == id_proyecto
    ]["ID_Hito"].values
    
    tareas_proyecto = tablas["dim_tareas"][
        tablas["dim_tareas"]["ID_Hito"].isin(hitos_proyecto)
    ]
    
    if len(tareas_proyecto) == 0:
        return 0.0
    
    tareas_retrasadas = (tareas_proyecto["SeRetraso"] == 1).sum()
    tareas_totales = len(tareas_proyecto)
    
    return (tareas_retrasadas / tareas_totales) * 100


def calcular_porcentaje_hitos_retrasados(id_proyecto: int, tablas: dict) -> float:
    """
    Métrica: PorcentajeHitosRetrasados
    Fórmula: (COUNT(HitosRetrasados) / COUNT(HitosTotales)) × 100
    Fuente: dim_hitos
    """
    hitos_proyecto = tablas["dim_hitos"][
        tablas["dim_hitos"]["ID_proyectos"] == id_proyecto
    ]
    
    if len(hitos_proyecto) == 0:
        return 0.0
    
    # Hito retrasado si RetrasoFinDias > 0
    hitos_retrasados = (hitos_proyecto["RetrasoFinDias"] > 0).sum()
    hitos_totales = len(hitos_proyecto)
    
    return (hitos_retrasados / hitos_totales) * 100


def calcular_costo_real_detallado(id_proyecto: int, tablas: dict) -> dict:
    """
    Métrica: CostoReal (desglosado)
    Fórmula: Σ(CostoPorHoraEmpleado × HorasReales) + Σ GastosFinancieros
    Fuente: dim_empleados, dim_finanzas, hechos_asignaciones
    """
    asignaciones = tablas["hechos_asignaciones"][
        tablas["hechos_asignaciones"]["ID_Proyecto"] == id_proyecto
    ]
    
    # Costo por horas trabajadas
    costo_horas = asignaciones["ValorHoras"].sum()
    
    # Gastos financieros del proyecto
    proyecto_hp = tablas["hechos_proyectos"][
        tablas["hechos_proyectos"]["ID_Proyecto"] == id_proyecto
    ]
    
    if len(proyecto_hp) > 0 and "ID_Gasto" in proyecto_hp.columns:
        id_gasto = proyecto_hp.iloc[0]["ID_Gasto"]
        if pd.notna(id_gasto):
            gasto = tablas["dim_gastos"][
                tablas["dim_gastos"]["ID_Finanza"] == id_gasto
            ]
            gasto_financiero = gasto["Monto"].sum() if len(gasto) > 0 else 0
        else:
            gasto_financiero = 0
    else:
        gasto_financiero = 0
    
    costo_total = costo_horas + gasto_financiero
    
    return {
        "costo_horas": float(costo_horas),
        "gasto_financiero": float(gasto_financiero),
        "costo_total": float(costo_total)
    }


def generar_dataframe_metricas_calculadas() -> pd.DataFrame:
    """
    Genera un DataFrame con todas las métricas calculadas dinámicamente
    para todos los proyectos
    """
    tablas = cargar_tablas_completas()
    proyectos_ids = tablas["dim_proyectos"]["ID_Proyecto"].unique()
    
    metricas_list = []
    
    for id_proyecto in proyectos_ids:
        try:
            costo_detalle = calcular_costo_real_detallado(id_proyecto, tablas)
            
            metricas = {
                "ID_Proyecto": id_proyecto,
                "DuracionRealDias": calcular_duracion_real_dias(id_proyecto, tablas),
                "NumeroDefectosEncontrados": calcular_numero_defectos_encontrados(id_proyecto, tablas),
                "ProductividadPromedio_Calculada": calcular_productividad_promedio(id_proyecto, tablas),
                "PorcentajeTareasRetrasadas_Calculada": calcular_porcentaje_tareas_retrasadas(id_proyecto, tablas),
                "PorcentajeHitosRetrasados_Calculada": calcular_porcentaje_hitos_retrasados(id_proyecto, tablas),
                "CostoReal_Horas": costo_detalle["costo_horas"],
                "CostoReal_Gastos": costo_detalle["gasto_financiero"],
                "CostoReal_Total_Calculado": costo_detalle["costo_total"],
            }
            metricas_list.append(metricas)
        except Exception as e:
            st.warning(f"Error calculando métricas para proyecto {id_proyecto}: {e}")
            continue
    
    return pd.DataFrame(metricas_list)


def obtener_estadisticas_metricas_calculadas() -> dict:
    """
    Retorna estadísticas agregadas de las métricas calculadas
    """
    df_metricas = generar_dataframe_metricas_calculadas()
    
    return {
        "duracion_promedio_dias": df_metricas["DuracionRealDias"].mean(),
        "defectos_promedio": df_metricas["NumeroDefectosEncontrados"].mean(),
        "defectos_total": df_metricas["NumeroDefectosEncontrados"].sum(),
        "productividad_calculada": df_metricas["ProductividadPromedio_Calculada"].mean(),
        "tareas_retrasadas_calculada": df_metricas["PorcentajeTareasRetrasadas_Calculada"].mean() / 100,
        "hitos_retrasados_calculada": df_metricas["PorcentajeHitosRetrasados_Calculada"].mean() / 100,
        "costo_real_promedio": df_metricas["CostoReal_Total_Calculado"].mean(),
    }
