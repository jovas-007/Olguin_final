from typing import Dict

import numpy as np
import pandas as pd


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

    cumplimiento = 1 - (proyectos["CosteReal"] - proyectos["Presupuesto"]) / proyectos[
        "Presupuesto"
    ]
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
        proyectos = proyectos.copy()
        proyectos["FechaFin"] = pd.to_datetime(proyectos[["AnioFin", "MesFin"]].assign(Dia=1))
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
