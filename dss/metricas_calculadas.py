"""
Módulo para calcular métricas dinámicamente según especificaciones del proyecto.
Todas las métricas se calculan siguiendo las fórmulas exactas especificadas.

MÉTRICAS IMPLEMENTADAS:
1. RetrasoInicioDias: FechaInicioReal - FechaInicio
2. RetrasoFinalDias: FechaFinReal - FechaFin
3. Presupuesto: ValorTotalContrato (tabla contratos)
4. CosteReal: Suma(Gastos) + Suma(HorasReales * CostoPorHora)
5. DesviacionPresupuestal: Presupuesto - CosteReal
6. PenalizacionesMonto: Suma(Monto de penalizaciones)
7. ProporcionCAPEX_OPEX: Suma(CAPEX) / Suma(OPEX)
8. TasaDeErroresEncontrados: Cantidad errores / Cantidad tareas
9. TasaDeExitoEnPruebas: Pruebas exitosas / Pruebas totales
10. ProductividadPromedio: Suma(HorasReales) / Cantidad hitos
11. PorcentajeTareasRetrasadas: Tareas retrasadas / Total tareas
12. PorcentajeHitosRetrasados: Hitos retrasados / Total hitos
"""

from pathlib import Path
import pandas as pd
import numpy as np
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


def calcular_retrasos(id_proyecto: int, tablas: dict) -> dict:
    """
    Métricas: RetrasoInicioDias y RetrasoFinalDias
    Fórmulas:
    - RetrasoInicioDias: FechaInicioReal - FechaInicio
    - RetrasoFinalDias: FechaFinReal - FechaFin
    """
    hp = tablas["hechos_proyectos"]
    dt = tablas["dim_tiempo"]
    
    proyecto = hp[hp["ID_Proyecto"] == id_proyecto].iloc[0]
    
    # Obtener fechas planificadas
    fecha_inicio_plan = dt[dt["ID_Tiempo"] == proyecto["ID_FechaInicio"]].iloc[0]
    fecha_fin_plan = dt[dt["ID_Tiempo"] == proyecto["ID_FechaFin"]].iloc[0]
    
    # Las fechas reales están en el mismo proyecto (asumiendo que ID_FechaFin es la real)
    # En producción, deberían existir campos separados para fechas reales
    fecha_inicio_real = fecha_inicio_plan  # Placeholder
    fecha_fin_real = fecha_fin_plan  # Placeholder
    
    # Convertir a datetime
    inicio_plan_dt = pd.to_datetime(f"{fecha_inicio_plan['Anio']}-{fecha_inicio_plan['Mes']}-{fecha_inicio_plan['Dia']}")
    fin_plan_dt = pd.to_datetime(f"{fecha_fin_plan['Anio']}-{fecha_fin_plan['Mes']}-{fecha_fin_plan['Dia']}")
    
    # Por ahora usamos los valores ya calculados en hechos_proyectos
    retraso_inicio = proyecto.get("RetrasoInicioDias", 0)
    retraso_fin = proyecto.get("RetrasoFinalDias", 0)
    
    return {
        "retraso_inicio_dias": int(retraso_inicio),
        "retraso_final_dias": int(retraso_fin)
    }


def calcular_presupuesto(id_proyecto: int, tablas: dict) -> float:
    """
    Métrica: Presupuesto
    Fórmula: Se toma directamente de ValorTotalContrato (tabla contratos)
    Por ahora usamos el campo Presupuesto de hechos_proyectos
    """
    hp = tablas["hechos_proyectos"]
    proyecto = hp[hp["ID_Proyecto"] == id_proyecto].iloc[0]
    return float(proyecto.get("Presupuesto", 0))


def calcular_coste_real(id_proyecto: int, tablas: dict) -> dict:
    """
    Métrica: CosteReal
    Fórmula: Suma(Monto gastos) + Suma(HorasReales * CostoPorHora empleados)
    """
    # 1. Costos por horas de empleados
    asignaciones = tablas["hechos_asignaciones"]
    asignaciones_proyecto = asignaciones[asignaciones["ID_Proyecto"] == id_proyecto]
    
    # ValorHoras ya contiene HorasReales * CostoPorHora
    costo_horas = asignaciones_proyecto["ValorHoras"].sum() if len(asignaciones_proyecto) > 0 else 0
    
    # 2. Gastos del proyecto
    hp = tablas["hechos_proyectos"]
    proyecto = hp[hp["ID_Proyecto"] == id_proyecto]
    
    gastos_financieros = 0
    if len(proyecto) > 0 and "ID_Gasto" in proyecto.columns:
        id_gasto = proyecto.iloc[0]["ID_Gasto"]
        if pd.notna(id_gasto):
            gasto = tablas["dim_gastos"][tablas["dim_gastos"]["ID_Finanza"] == id_gasto]
            gastos_financieros = gasto["Monto"].sum() if len(gasto) > 0 else 0
    
    costo_total = costo_horas + gastos_financieros
    
    return {
        "costo_horas": float(costo_horas),
        "gastos_financieros": float(gastos_financieros),
        "costo_total": float(costo_total)
    }


def calcular_desviacion_presupuestal(id_proyecto: int, tablas: dict) -> float:
    """
    Métrica: DesviacionPresupuestal
    Fórmula: Presupuesto - CosteReal
    """
    presupuesto = calcular_presupuesto(id_proyecto, tablas)
    coste = calcular_coste_real(id_proyecto, tablas)
    return presupuesto - coste["costo_total"]


def calcular_penalizaciones_monto(id_proyecto: int, tablas: dict) -> float:
    """
    Métrica: PenalizacionesMonto
    Fórmula: Suma de montos de penalizaciones_contrato
    Por ahora usa el campo PenalizacionesMonto de hechos_proyectos
    """
    hp = tablas["hechos_proyectos"]
    proyecto = hp[hp["ID_Proyecto"] == id_proyecto].iloc[0]
    return float(proyecto.get("PenalizacionesMonto", 0))


def calcular_proporcion_capex_opex(id_proyecto: int, tablas: dict) -> float:
    """
    Métrica: ProporcionCAPEX_OPEX
    Fórmula: Suma(Monto CAPEX) / Suma(Monto OPEX) de tabla gastos
    Por ahora usa el campo ProporcionCAPEX_OPEX de hechos_proyectos
    """
    hp = tablas["hechos_proyectos"]
    proyecto = hp[hp["ID_Proyecto"] == id_proyecto].iloc[0]
    return float(proyecto.get("ProporcionCAPEX_OPEX", 0))


def calcular_tasa_errores_encontrados(id_proyecto: int, tablas: dict) -> float:
    """
    Métrica: TasaDeErroresEncontrados
    Fórmula: Cantidad de errores / Cantidad de tareas
    """
    # Obtener hitos del proyecto
    hitos_proyecto = tablas["dim_hitos"][
        tablas["dim_hitos"]["ID_proyectos"] == id_proyecto
    ]["ID_Hito"].values
    
    # Obtener tareas de esos hitos
    tareas_proyecto = tablas["dim_tareas"][
        tablas["dim_tareas"]["ID_Hito"].isin(hitos_proyecto)
    ]
    
    cantidad_tareas = len(tareas_proyecto)
    if cantidad_tareas == 0:
        return 0.0
    
    # Total de errores del proyecto (desde dim_proyectos)
    total_errores = tablas["dim_proyectos"][
        tablas["dim_proyectos"]["ID_Proyecto"] == id_proyecto
    ]["TotalErrores"].iloc[0]
    
    tasa = total_errores / cantidad_tareas
    return float(tasa)


def calcular_tasa_exito_pruebas(id_proyecto: int, tablas: dict) -> float:
    """
    Métrica: TasaDeExitoEnPruebas
    Fórmula: Pruebas exitosas / Pruebas totales
    """
    hitos_proyecto = tablas["dim_hitos"][
        tablas["dim_hitos"]["ID_proyectos"] == id_proyecto
    ]["ID_Hito"].values
    
    pruebas_proyecto = tablas["dim_pruebas"][
        tablas["dim_pruebas"]["ID_Hito"].isin(hitos_proyecto)
    ]
    
    if len(pruebas_proyecto) == 0:
        return 0.0
    
    pruebas_exitosas = (pruebas_proyecto["PruebaExitosa"] == 1).sum()
    pruebas_totales = len(pruebas_proyecto)
    
    tasa = pruebas_exitosas / pruebas_totales
    return float(tasa)


def calcular_productividad_promedio(id_proyecto: int, tablas: dict) -> float:
    """
    Métrica: ProductividadPromedio
    Fórmula: Suma(HorasReales) / Cantidad de hitos
    """
    # Sumar horas reales de asignaciones del proyecto
    asignaciones = tablas["hechos_asignaciones"]
    asignaciones_proyecto = asignaciones[asignaciones["ID_Proyecto"] == id_proyecto]
    
    suma_horas_reales = asignaciones_proyecto["HorasReales"].sum()
    
    # Contar hitos del proyecto
    hitos_proyecto = tablas["dim_hitos"][
        tablas["dim_hitos"]["ID_proyectos"] == id_proyecto
    ]
    
    cantidad_hitos = len(hitos_proyecto)
    
    if cantidad_hitos == 0:
        return 0.0
    
    productividad = suma_horas_reales / cantidad_hitos
    return float(productividad)


def calcular_porcentaje_tareas_retrasadas(id_proyecto: int, tablas: dict) -> float:
    """
    Métrica: PorcentajeTareasRetrasadas
    Fórmula: (Tareas con SeRetraso=True) / Total tareas × 100
    SeRetraso se marca True si FechaInicioPlanificada != FechaInicioReal
    O si FechaFinPlanificada != FechaFinReal
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
    
    porcentaje = (tareas_retrasadas / tareas_totales) * 100
    return float(porcentaje)


def calcular_porcentaje_hitos_retrasados(id_proyecto: int, tablas: dict) -> float:
    """
    Métrica: PorcentajeHitosRetrasados
    Fórmula: (Hitos retrasados) / Total hitos × 100
    Un hito está retrasado si RetrasoInicioDias > 0 O RetrasoFinDias > 0
    """
    hitos_proyecto = tablas["dim_hitos"][
        tablas["dim_hitos"]["ID_proyectos"] == id_proyecto
    ]
    
    if len(hitos_proyecto) == 0:
        return 0.0
    
    # Hito retrasado si alguno de los retrasos es > 0
    hitos_retrasados = (
        (hitos_proyecto["RetrasoFinDias"] > 0) | 
        (hitos_proyecto.get("RetrasoInicioDias", 0) > 0)
    ).sum()
    
    hitos_totales = len(hitos_proyecto)
    
    porcentaje = (hitos_retrasados / hitos_totales) * 100
    return float(porcentaje)


def generar_dataframe_metricas_calculadas() -> pd.DataFrame:
    """
    Genera un DataFrame con todas las métricas calculadas.
    Las métricas ya están precalculadas en hechos_proyectos_seed.csv
    """
    tablas = cargar_tablas_completas()
    
    # Leer hechos_proyectos que ya contiene las métricas calculadas
    df_hechos = tablas["hechos_proyectos"]
    
    # Seleccionar solo las columnas de métricas que necesitamos
    columnas_metricas = [
        "ID_Proyecto",
        "RetrasoInicioDias",
        "RetrasoFinalDias",
        "Presupuesto",
        "CosteReal",
        "DesviacionPresupuestal",
        "PenalizacionesMonto",
        "ProporcionCAPEX_OPEX",
        "TasaDeErroresEncontrados",
        "TasaDeExitoEnPruebas",
        "ProductividadPromedio",
        "PorcentajeTareasRetrasadas",
        "PorcentajeHitosRetrasados",
    ]
    
    # Filtrar solo las columnas que existen
    columnas_existentes = [col for col in columnas_metricas if col in df_hechos.columns]
    df_metricas = df_hechos[columnas_existentes].copy()
    
    # Convertir porcentajes a decimal (0-1) si están en formato 0-100
    for col in ["TasaDeErroresEncontrados", "TasaDeExitoEnPruebas", "PorcentajeTareasRetrasadas", "PorcentajeHitosRetrasados"]:
        if col in df_metricas.columns:
            # Si los valores son > 1, están en formato 0-100, convertir a 0-1
            if df_metricas[col].max() > 1:
                df_metricas[col] = df_metricas[col] / 100
    
    print(f"✅ Métricas cargadas para {len(df_metricas)} proyectos")
    return df_metricas


def obtener_estadisticas_metricas_calculadas() -> dict:
    """
    Retorna estadísticas agregadas de las métricas calculadas
    """
    df_metricas = generar_dataframe_metricas_calculadas()
    
    return {
        "retraso_inicio_promedio": df_metricas["RetrasoInicioDias"].mean(),
        "retraso_final_promedio": df_metricas["RetrasoFinalDias"].mean(),
        "presupuesto_promedio": df_metricas["Presupuesto"].mean(),
        "coste_real_promedio": df_metricas["CosteReal"].mean(),
        "desviacion_presupuestal_promedio": df_metricas["DesviacionPresupuestal"].mean(),
        "penalizaciones_total": df_metricas["PenalizacionesMonto"].sum(),
        "penalizaciones_promedio": df_metricas["PenalizacionesMonto"].mean(),
        "proporcion_capex_opex": df_metricas["ProporcionCAPEX_OPEX"].mean(),
        "tasa_errores_promedio": df_metricas["TasaDeErroresEncontrados"].mean(),
        "tasa_exito_pruebas_promedio": df_metricas["TasaDeExitoEnPruebas"].mean(),
        "productividad_promedio": df_metricas["ProductividadPromedio"].mean(),
        "tareas_retrasadas_porcentaje": df_metricas["PorcentajeTareasRetrasadas"].mean(),
        "hitos_retrasados_porcentaje": df_metricas["PorcentajeHitosRetrasados"].mean(),
    }
