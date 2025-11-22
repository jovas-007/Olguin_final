import pandas as pd
import streamlit as st

from dss.analytics import build_olap_views, get_detail_table, get_kpis
from dss.config import KPI_TARGETS
from dss.prediction import calcular_sigma, entrenar_modelo, rayleigh_curve
from dss.ui.components import mostrar_tarjeta_kpi


def render_scorecard(df_proyectos: pd.DataFrame, df_asignaciones: pd.DataFrame, filtros: dict):
    kpis = get_kpis(df_proyectos, df_asignaciones, filtros)
    vistas = build_olap_views(df_proyectos, df_asignaciones, filtros)

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


def render_detalle(df_proyectos: pd.DataFrame, df_asignaciones: pd.DataFrame, filtros: dict):
    vistas = build_olap_views(df_proyectos, df_asignaciones, filtros)
    detalle = get_detail_table(df_proyectos, filtros)

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


def render_prediccion(df_proyectos: pd.DataFrame, kpis: dict):
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
                    "ProductividadPromedio": kpis.get("productividad_promedio") or 0.75,
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
