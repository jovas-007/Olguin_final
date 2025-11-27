import pandas as pd
import streamlit as st

from dss.analytics import build_olap_views, get_detail_table, get_kpis
from dss.config import KPI_TARGETS
from dss.prediction import (
    calcular_sigma,
    entrenar_modelo,
    rayleigh_curve,
    obtener_metricas_modelo,
    clasificar_nivel_riesgo,
    generar_recomendaciones,
    generar_plan_testing,
    buscar_proyectos_similares
)
from dss.predicciones_simple import generar_todas_predicciones
from dss.okrs import calcular_todos_okrs
from dss.ui.components import mostrar_tarjeta_kpi
from dss.metricas_calculadas import (
    generar_dataframe_metricas_calculadas,
    obtener_estadisticas_metricas_calculadas,
    cargar_tablas_completas
)


def render_scorecard(df_proyectos: pd.DataFrame, df_asignaciones: pd.DataFrame, filtros: dict):
    kpis = get_kpis(df_proyectos, df_asignaciones, filtros)
    vistas = build_olap_views(df_proyectos, df_asignaciones, filtros)
    
    # Generar predicciones y recomendaciones
    predicciones = generar_todas_predicciones(kpis, vistas)

    # Header principal con diseño mejorado
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 15px; margin-bottom: 30px;'>
            <h1 style='color: white; margin: 0; text-align: center; font-size: 2.5em;'>
                Balanced Scorecard
            </h1>
            <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 10px 0 0 0; font-size: 1.1em;'>
                Cuadro de Mando Integral - Análisis Estratégico de Desempeño
            </p>
            <p style='color: rgba(255,255,255,0.85); text-align: center; margin: 8px 0 0 0; font-size: 0.95em;'>
                <strong>Misión:</strong> Optimizar procesos con tecnología | 
                <strong>Visión:</strong> Decisiones basadas en datos y excelencia sostenible
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Perspectivas con diseño de tarjetas modernas
    st.markdown("---")
    
    # PERSPECTIVA FINANCIERA
    st.markdown("""
        <div style='background: linear-gradient(to right, #11998e, #38ef7d); 
                    padding: 15px 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0; font-size: 1.8em;'>Perspectiva Financiera</h2>
            <p style='color: rgba(255,255,255,0.95); margin: 5px 0 0 0;'>
                Eficiencia financiera, sostenibilidad y optimización de recursos
            </p>
            <p style='color: rgba(255,255,255,0.85); margin: 5px 0 0 0; font-size: 0.9em; font-style: italic;'>
                Visión: Excelencia sostenible en gestión económica de proyectos
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_fin1, col_fin2, col_fin3 = st.columns(3)
    with col_fin1:
        mostrar_tarjeta_kpi(
            "Cumplimiento de presupuesto",
            kpis["cumplimiento_presupuesto"],
            KPI_TARGETS["cumplimiento_presupuesto"],
            "Refleja eficiencia financiera alineada a sostenibilidad y optimización.",
        )
    with col_fin2:
        mostrar_tarjeta_kpi(
            "Desviación presupuestal promedio",
            kpis["desviacion_presupuestal"],
            KPI_TARGETS["desviacion_presupuestal"],
            "Control estricto de costos para mantener rentabilidad y resiliencia.",
            menor_mejor=True
        )
    with col_fin3:
        mostrar_tarjeta_kpi(
            "Penalizaciones sobre presupuesto",
            kpis["penalizaciones_sobre_presupuesto"],
            KPI_TARGETS["penalizaciones_sobre_presupuesto"],
            "Minimiza riesgos económicos y refuerza acuerdos de calidad.",
            menor_mejor=True
        )
    
    # Recomendaciones Financieras
    pred_fin = predicciones["financiera"]
    st.markdown(f"""
        <div style='background: rgba(17, 153, 142, 0.1); padding: 15px; border-radius: 8px; 
                    border-left: 4px solid #11998e; margin-top: 15px;'>
            <h4 style='margin: 0 0 10px 0; color: #11998e;'>
                {pred_fin['color']} Predicción de Riesgo: {pred_fin['nivel']}
            </h4>
            <p style='margin: 5px 0; font-size: 0.9em;'><strong>Score de Riesgo:</strong> {pred_fin['score']:.1f}/100</p>
            <p style='margin: 10px 0 5px 0; font-weight: 600;'>Recomendaciones:</p>
            <ul style='margin: 5px 0; padding-left: 20px;'>
                {"".join([f"<li>{rec}</li>" for rec in pred_fin['recomendaciones']])}
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # PERSPECTIVA DEL CLIENTE
    st.markdown("""
        <div style='background: linear-gradient(to right, #2980b9, #6dd5fa); 
                    padding: 15px 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0; font-size: 1.8em;'>Perspectiva del Cliente</h2>
            <p style='color: rgba(255,255,255,0.95); margin: 5px 0 0 0;'>
                Cumplimiento de compromisos, confianza y fidelización
            </p>
            <p style='color: rgba(255,255,255,0.85); margin: 5px 0 0 0; font-size: 0.9em; font-style: italic;'>
                Visión: Decisiones basadas en datos para maximizar satisfacción
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_cli1, col_cli2 = st.columns(2)
    with col_cli1:
        mostrar_tarjeta_kpi(
            "Proyectos entregados a tiempo",
            kpis["proyectos_a_tiempo"],
            KPI_TARGETS["proyectos_a_tiempo"],
            "Cumplimiento de compromisos aumenta confianza y fidelidad.",
        )
    with col_cli2:
        mostrar_tarjeta_kpi(
            "Proyectos NO cancelados",
            1 - kpis["proyectos_cancelados"],
            1 - KPI_TARGETS["proyectos_cancelados"],
            "Gestión de riesgos temprana evita cancelaciones y refuerza la reputación.",
            menor_mejor=False  # Mayor % de NO cancelados es mejor
        )
    
    # Recomendaciones de Satisfacción del Cliente
    pred_cli = predicciones["cliente"]
    st.markdown(f"""
        <div style='background: rgba(41, 128, 185, 0.1); padding: 15px; border-radius: 8px; 
                    border-left: 4px solid #2980b9; margin-top: 15px;'>
            <h4 style='margin: 0 0 10px 0; color: #2980b9;'>
                {pred_cli['color']} Predicción de Satisfacción: {pred_cli['nivel']}
            </h4>
            <p style='margin: 5px 0; font-size: 0.9em;'><strong>Score de Satisfacción:</strong> {pred_cli['score']:.1f}/100</p>
            <p style='margin: 10px 0 5px 0; font-weight: 600;'>Recomendaciones:</p>
            <ul style='margin: 5px 0; padding-left: 20px;'>
                {"".join([f"<li>{rec}</li>" for rec in pred_cli['recomendaciones']])}
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # PERSPECTIVA DE PROCESOS INTERNOS
    st.markdown("""
        <div style='background: linear-gradient(to right, #f857a6, #ff5858); 
                    padding: 15px 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0; font-size: 1.8em;'>Perspectiva de Procesos Internos</h2>
            <p style='color: rgba(255,255,255,0.95); margin: 5px 0 0 0;'>
                Operación ágil, trazabilidad y calidad del producto
            </p>
            <p style='color: rgba(255,255,255,0.85); margin: 5px 0 0 0; font-size: 0.9em; font-style: italic;'>
                Misión: Optimizar procesos internos con tecnología avanzada
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_proc1, col_proc2, col_proc3 = st.columns(3)
    with col_proc1:
        mostrar_tarjeta_kpi(
            "Tareas completadas a tiempo",
            1 - kpis["porcentaje_tareas_retrasadas"],
            1 - KPI_TARGETS["porcentaje_tareas_retrasadas"],
            "Menos retrasos implica operación ágil y trazable.",
        )
    with col_proc2:
        mostrar_tarjeta_kpi(
            "Hitos completados a tiempo",
            1 - kpis["porcentaje_hitos_retrasados"],
            1 - KPI_TARGETS["porcentaje_hitos_retrasados"],
            "Entrega disciplinada de hitos acelera valor al cliente.",
        )
    with col_proc3:
        mostrar_tarjeta_kpi(
            "Calidad del código",
            1 - kpis["tasa_errores"],
            1 - KPI_TARGETS["tasa_errores"],
            "Calidad del producto mejora satisfacción y reduce reprocesos.",
        )
    
    # Recomendaciones de Eficiencia de Procesos
    pred_proc = predicciones["procesos"]
    st.markdown(f"""
        <div style='background: rgba(248, 87, 166, 0.1); padding: 15px; border-radius: 8px; 
                    border-left: 4px solid #f857a6; margin-top: 15px;'>
            <h4 style='margin: 0 0 10px 0; color: #f857a6;'>
                {pred_proc['color']} Predicción de Eficiencia: {pred_proc['nivel']}
            </h4>
            <p style='margin: 5px 0; font-size: 0.9em;'><strong>Score de Eficiencia:</strong> {pred_proc['score']:.1f}/100</p>
            <p style='margin: 10px 0 5px 0; font-weight: 600;'>Recomendaciones:</p>
            <ul style='margin: 5px 0; padding-left: 20px;'>
                {"".join([f"<li>{rec}</li>" for rec in pred_proc['recomendaciones']])}
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # PERSPECTIVA DE APRENDIZAJE E INNOVACIÓN
    st.markdown("""
        <div style='background: linear-gradient(to right, #fa709a, #fee140); 
                    padding: 15px 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0; font-size: 1.8em;'>Perspectiva de Aprendizaje e Innovación</h2>
            <p style='color: rgba(255,255,255,0.95); margin: 5px 0 0 0;'>
                Colaboración interdisciplinaria, mejora continua y escalabilidad
            </p>
            <p style='color: rgba(255,255,255,0.85); margin: 5px 0 0 0; font-size: 0.9em; font-style: italic;'>
                Visión: Excelencia sostenible mediante desarrollo del capital humano
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_learn1, col_learn2, col_learn3 = st.columns(3)
    with col_learn1:
        mostrar_tarjeta_kpi(
            "Productividad promedio",
            kpis["productividad_promedio"],
            KPI_TARGETS["productividad_promedio"],
            "Colaboración interdisciplinaria y mejora continua.",
        )
    with col_learn2:
        mostrar_tarjeta_kpi(
            "Tasa de éxito en pruebas",
            kpis["tasa_exito_pruebas"],
            KPI_TARGETS["tasa_exito_pruebas"],
            "Pruebas efectivas aseguran software confiable e innovador.",
        )
    with col_learn3:
        mostrar_tarjeta_kpi(
            "Relación horas reales / planificadas",
            kpis["horas_relacion"],
            KPI_TARGETS["horas_relacion"],
            "Planificación precisa favorece proyectos medibles y escalables.",
        )
    
    # Recomendaciones de Desarrollo del Equipo
    pred_learn = predicciones["aprendizaje"]
    st.markdown(f"""
        <div style='background: rgba(250, 112, 154, 0.1); padding: 15px; border-radius: 8px; 
                    border-left: 4px solid #fa709a; margin-top: 15px;'>
            <h4 style='margin: 0 0 10px 0; color: #fa709a;'>
                {pred_learn['color']} Predicción de Capacidad del Equipo: {pred_learn['nivel']}
            </h4>
            <p style='margin: 5px 0; font-size: 0.9em;'><strong>Score de Capacidad:</strong> {pred_learn['score']:.1f}/100</p>
            <p style='margin: 10px 0 5px 0; font-weight: 600;'>Recomendaciones:</p>
            <ul style='margin: 5px 0; padding-left: 20px;'>
                {"".join([f"<li>{rec}</li>" for rec in pred_learn['recomendaciones']])}
            </ul>
        </div>
    """, unsafe_allow_html=True)


def render_analisis_visual(df_proyectos: pd.DataFrame, df_asignaciones: pd.DataFrame, filtros: dict):
    """Vista de análisis visual estratégico con gráficos y visualizaciones clave"""
    kpis = get_kpis(df_proyectos, df_asignaciones, filtros)
    vistas = build_olap_views(df_proyectos, df_asignaciones, filtros)
    
    # Header
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px 25px; border-radius: 12px; margin: 25px 0;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <h2 style='color: white; margin: 0; font-size: 2em; font-weight: 600;'>Análisis Visual Estratégico</h2>
            <p style='color: rgba(255,255,255,0.95); margin: 8px 0 0 0; font-size: 1.05em;'>
                Dashboard de indicadores clave de rendimiento y tendencias operativas
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Primera fila de visualizaciones
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        st.markdown("""
            <div style='background: linear-gradient(to right, #11998e, #38ef7d); 
                        padding: 12px 18px; border-radius: 8px; margin-bottom: 12px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0; color: white; font-weight: 600;'>Presupuesto vs Coste Real</h4>
                <p style='margin: 4px 0 0 0; color: rgba(255,255,255,0.9); font-size: 0.9em;'>
                    Análisis comparativo por proyecto
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.bar_chart(
            vistas["barras_presupuesto"].set_index("CodigoProyecto")[["Presupuesto", "CosteReal"]],
            use_container_width=True,
            height=400
        )
        st.caption("Comparación financiera para identificar desviaciones presupuestales y optimizar control de costos.")
    
    with col_viz2:
        st.markdown("""
            <div style='background: linear-gradient(to right, #2980b9, #6dd5fa); 
                        padding: 12px 18px; border-radius: 8px; margin-bottom: 12px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0; color: white; font-weight: 600;'>Evolución de Entregas a Tiempo</h4>
                <p style='margin: 4px 0 0 0; color: rgba(255,255,255,0.9); font-size: 0.9em;'>
                    Tendencia mensual de cumplimiento
                </p>
            </div>
        """, unsafe_allow_html=True)
        if not vistas["proyectos_a_tiempo"].empty and len(vistas["proyectos_a_tiempo"]) > 0:
            if "Fecha" in vistas["proyectos_a_tiempo"].columns and "A_Tiempo" in vistas["proyectos_a_tiempo"].columns:
                chart_data = vistas["proyectos_a_tiempo"].set_index("Fecha")[["A_Tiempo"]]
                st.line_chart(chart_data, use_container_width=True, height=400)
                st.caption("Seguimiento temporal del cumplimiento de plazos para gestión proactiva de riesgos.")
            else:
                st.warning("Datos de evolución temporal incompletos - faltan columnas requeridas.")
        else:
            st.info("Sin datos suficientes para mostrar evolución mensual de entregas a tiempo.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Segunda fila de visualizaciones
    col_viz3, col_viz4 = st.columns(2)
    
    with col_viz3:
        st.markdown("""
            <div style='background: linear-gradient(to right, #f857a6, #ff5858); 
                        padding: 12px 18px; border-radius: 8px; margin-bottom: 12px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0; color: white; font-weight: 600;'>Distribución de Retrasos</h4>
                <p style='margin: 4px 0 0 0; color: rgba(255,255,255,0.9); font-size: 0.9em;'>
                    Retrasos de inicio vs finalización
                </p>
            </div>
        """, unsafe_allow_html=True)
        if not vistas["retrasos"].empty:
            st.bar_chart(
                vistas["retrasos"].set_index("CodigoProyecto")[["RetrasoInicioDias", "RetrasoFinalDias"]],
                use_container_width=True,
                height=400
            )
            st.caption("Identificación de proyectos críticos para reasignación de recursos y ajuste de planificación.")
        else:
            st.info("No hay datos de retrasos disponibles para el filtro actual.")
    
    with col_viz4:
        st.markdown("""
            <div style='background: linear-gradient(to right, #fa709a, #fee140); 
                        padding: 12px 18px; border-radius: 8px; margin-bottom: 12px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0; color: white; font-weight: 600;'>Productividad por Rol</h4>
                <p style='margin: 4px 0 0 0; color: rgba(255,255,255,0.9); font-size: 0.9em;'>
                    Relación horas reales/planificadas
                </p>
            </div>
        """, unsafe_allow_html=True)
        if not vistas["productividad_por_rol"].empty:
            data = vistas["productividad_por_rol"].copy()
            data["Relacion"] = data["HorasReales"] / data["HorasPlanificadas"]
            st.bar_chart(data.set_index("Rol")["Relacion"], use_container_width=True, height=400)
            st.caption("Análisis de eficiencia por rol para optimización de cargas de trabajo y formación dirigida.")
        else:
            st.info("No hay datos de asignaciones disponibles para el filtro actual.")


def render_detalle(df_proyectos: pd.DataFrame, df_asignaciones: pd.DataFrame, filtros: dict):
    vistas = build_olap_views(df_proyectos, df_asignaciones, filtros)
    detalle = get_detail_table(df_proyectos, filtros)

    # Header principal
    st.markdown("""
        <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                    padding: 25px; border-radius: 12px; margin-bottom: 25px;'>
            <h1 style='color: white; margin: 0; font-size: 2.2em;'>Análisis Detallado OLAP</h1>
            <p style='color: rgba(255,255,255,0.95); margin: 8px 0 0 0; font-size: 1.05em;'>
                Vistas multidimensionales con drill-down, roll-up, slicing, dicing y pivot
            </p>
            <p style='color: rgba(255,255,255,0.85); margin: 8px 0 0 0; font-size: 0.95em;'>
                <strong>Misión:</strong> Optimizar procesos mediante análisis tecnológico avanzado | 
                <strong>Visión:</strong> Datos accionables para decisiones estratégicas
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabla detallada
    st.subheader("Tabla Consolidada de Proyectos")
    st.dataframe(detalle, use_container_width=True, height=400)
    st.caption("Datos consolidados por proyecto incluyendo tiempos, costos, recursos y desviaciones.")

    st.markdown("---")
    
    # Sección de análisis de tiempos y retrasos
    st.subheader("Análisis Temporal y Retrasos")
    st.caption("Evaluación de cumplimiento de plazos y eficiencia de ejecución")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_tiempo1, col_tiempo2 = st.columns(2)
    
    with col_tiempo1:
        st.markdown("**Retrasos de Inicio vs Finalización**")
        if not vistas["retrasos"].empty:
            st.bar_chart(
                vistas["retrasos"].set_index("CodigoProyecto")[["RetrasoInicioDias", "RetrasoFinalDias"]],
                use_container_width=True,
                height=400
            )
            st.caption("Identifica proyectos críticos con retrasos significativos para reasignación de recursos.")
        else:
            st.info("No hay datos de retrasos disponibles para el filtro actual.")
    
    with col_tiempo2:
        st.markdown("**Duración Real vs Planificada**")
        # Calcular duración desde las fechas
        fechas_disponibles = all(col in df_proyectos.columns for col in ["AnioInicio", "MesInicio", "AnioFin", "MesFin", "RetrasoFinalDias"])
        if not df_proyectos.empty and fechas_disponibles:
            proyectos_filtrados = df_proyectos[df_proyectos["CodigoProyecto"].isin(detalle["CodigoProyecto"])].copy()
            if not proyectos_filtrados.empty:
                # Duración planificada en meses
                proyectos_filtrados["Planificado"] = ((proyectos_filtrados["AnioFin"] - proyectos_filtrados["AnioInicio"]) * 12 + 
                                                       (proyectos_filtrados["MesFin"] - proyectos_filtrados["MesInicio"]))
                # Duración real considera retrasos (convertir días a meses)
                proyectos_filtrados["Real"] = proyectos_filtrados["Planificado"] + (proyectos_filtrados["RetrasoFinalDias"] / 30)
                
                duracion_comp = proyectos_filtrados[["CodigoProyecto", "Planificado", "Real"]]
                st.bar_chart(
                    duracion_comp.set_index("CodigoProyecto")[["Planificado", "Real"]],
                    use_container_width=True,
                    height=400
                )
                st.caption("Duración en meses - comparación entre planificado y real (con retrasos) para mejorar estimaciones.")
            else:
                st.info("No hay proyectos con datos de duración en el filtro actual.")
        else:
            st.info("No hay datos de duración disponibles para comparar.")

    st.markdown("---")

    # Sección de análisis de recursos y productividad
    st.subheader("Gestión de Recursos Humanos")
    st.caption("Eficiencia y aprovechamiento de capital humano")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_recursos1, col_recursos2 = st.columns(2)
    
    with col_recursos1:
        st.markdown("**Productividad por Rol**")
        if not vistas["productividad_por_rol"].empty:
            data = vistas["productividad_por_rol"].copy()
            data["Relacion"] = data["HorasReales"] / data["HorasPlanificadas"]
            st.bar_chart(data.set_index("Rol")["Relacion"], use_container_width=True, height=400)
            st.caption("Eficiencia por rol para optimización de cargas de trabajo y formación dirigida.")
        else:
            st.info("Sin datos de asignaciones para el filtro actual.")
    
    with col_recursos2:
        st.markdown("**Horas Planificadas vs Reales**")
        if not vistas["asignaciones"].empty:
            pivot = vistas["asignaciones"].pivot_table(
                index="CodigoProyecto",
                values=["HorasPlanificadas", "HorasReales"],
                aggfunc="sum",
            )
            st.bar_chart(pivot, use_container_width=True, height=400)
            st.caption("Analiza desviaciones operativas para ajustar estimaciones futuras de esfuerzo.")
        else:
            st.info("No hay asignaciones para mostrar en el rango seleccionado.")

    st.markdown("---")

    # Sección de análisis financiero detallado
    st.subheader("Análisis Financiero Comparativo")
    st.caption("Control presupuestal y rentabilidad de proyectos")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_fin1, col_fin2 = st.columns(2)
    
    with col_fin1:
        st.markdown("**Desviación Presupuestal**")
        if not detalle.empty and "DesviacionPresupuestal" in detalle.columns:
            desv_data = detalle[["CodigoProyecto", "DesviacionPresupuestal"]].copy()
            st.bar_chart(
                desv_data.set_index("CodigoProyecto")["DesviacionPresupuestal"],
                use_container_width=True,
                height=400
            )
            st.caption("Proyectos con mayor desviación presupuestal requieren análisis de causas raíz.")
        else:
            st.info("No hay datos de desviación presupuestal disponibles.")
    
    with col_fin2:
        st.markdown("**Penalizaciones vs Presupuesto**")
        pen_disponible = "PenalizacionesMonto" in df_proyectos.columns and "Presupuesto" in df_proyectos.columns
        if not df_proyectos.empty and pen_disponible:
            proyectos_filtrados = df_proyectos[df_proyectos["CodigoProyecto"].isin(detalle["CodigoProyecto"])].copy()
            if not proyectos_filtrados.empty:
                pen_data = proyectos_filtrados[["CodigoProyecto", "PenalizacionesMonto", "Presupuesto"]].copy()
                # Evitar división por cero
                pen_data = pen_data[pen_data["Presupuesto"] > 0]
                if not pen_data.empty:
                    pen_data["Porcentaje_Penalizacion"] = (pen_data["PenalizacionesMonto"] / pen_data["Presupuesto"]) * 100
                    st.bar_chart(
                        pen_data.set_index("CodigoProyecto")["Porcentaje_Penalizacion"],
                        use_container_width=True,
                        height=400
                    )
                    st.caption("Penalizaciones como porcentaje del presupuesto - indicador de riesgo contractual.")
                else:
                    st.info("No hay proyectos con presupuesto válido.")
            else:
                st.info("No hay proyectos con datos de penalizaciones en el filtro actual.")
        else:
            st.info("No hay datos de penalizaciones disponibles.")

    st.markdown("---")

    # Sección de calidad y errores
    st.subheader("Métricas de Calidad y Testing")
    st.caption("Evaluación de calidad del producto y efectividad de pruebas")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_cal1, col_cal2 = st.columns(2)
    
    with col_cal1:
        st.markdown("**Total de Errores por Proyecto**")
        errores_disponible = "TotalErrores" in df_proyectos.columns
        if not df_proyectos.empty and errores_disponible:
            proyectos_filtrados = df_proyectos[df_proyectos["CodigoProyecto"].isin(detalle["CodigoProyecto"])].copy()
            if not proyectos_filtrados.empty:
                errores_data = proyectos_filtrados[["CodigoProyecto", "TotalErrores"]].copy()
                st.bar_chart(
                    errores_data.set_index("CodigoProyecto")["TotalErrores"],
                    use_container_width=True,
                    height=400
                )
                st.caption("Proyectos con mayor cantidad de errores requieren refuerzo en QA y revisión de procesos.")
            else:
                st.info("No hay proyectos con datos de errores en el filtro actual.")
        else:
            st.info("No hay datos de errores disponibles.")
    
    with col_cal2:
        st.markdown("**Tasa de Éxito en Pruebas**")
        pruebas_disponible = "TasaDeExitoEnPruebas" in df_proyectos.columns
        if not df_proyectos.empty and pruebas_disponible:
            proyectos_filtrados = df_proyectos[df_proyectos["CodigoProyecto"].isin(detalle["CodigoProyecto"])].copy()
            if not proyectos_filtrados.empty:
                pruebas_data = proyectos_filtrados[["CodigoProyecto", "TasaDeExitoEnPruebas"]].copy()
                # Convertir a porcentaje
                pruebas_data["Tasa_Exito"] = pruebas_data["TasaDeExitoEnPruebas"] * 100
                st.bar_chart(
                    pruebas_data.set_index("CodigoProyecto")["Tasa_Exito"],
                    use_container_width=True,
                    height=400
                )
                st.caption("Mayor tasa de éxito indica mejor calidad de código y testing más efectivo.")
            else:
                st.info("No hay proyectos con datos de pruebas en el filtro actual.")
        else:
            st.info("No hay datos de pruebas disponibles.")



def render_prediccion(df_proyectos: pd.DataFrame, kpis: dict):
    st.markdown("""
        <div style='background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%); 
                    padding: 25px; border-radius: 12px; margin-bottom: 25px;'>
            <h1 style='color: white; margin: 0; font-size: 2.2em;'> Predicción de Defectos con IA</h1>
            <p style='color: rgba(255,255,255,0.95); margin: 8px 0 0 0; font-size: 1.05em;'>
                Modelo de Machine Learning basado en distribución de Rayleigh
            </p>
            <p style='color: rgba(255,255,255,0.85); margin: 8px 0 0 0; font-size: 0.95em;'>
                <strong>Misión:</strong> Optimizar calidad mediante predicción tecnológica | 
                <strong>Visión:</strong> Prevención proactiva basada en datos históricos
            </p>
        </div>
    """, unsafe_allow_html=True)

    modelo = entrenar_modelo(df_proyectos)
    metricas_modelo = obtener_metricas_modelo(df_proyectos, modelo)
    
    # Mostrar confianza del modelo
    col_conf1, col_conf2, col_conf3 = st.columns(3)
    with col_conf1:
        st.metric("R² Score", f"{metricas_modelo['r2']:.3f}", help="Capacidad predictiva del modelo (0-1)")
    with col_conf2:
        st.metric("RMSE", f"{metricas_modelo['rmse']:.1f}", help="Error cuadrático medio")
    with col_conf3:
        confianza_color = "[+]" if metricas_modelo['confianza'] == "Alta" else "[~]" if metricas_modelo['confianza'] == "Media" else "[-]"
        st.metric(f"{confianza_color} Confianza", metricas_modelo['confianza'], help="Nivel de confianza de las predicciones")

    st.divider()

    with st.form("prediccion_form", clear_on_submit=False):
        st.subheader("Parámetros del Proyecto")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            presupuesto = st.number_input("Presupuesto estimado ($)", value=100000.0, step=5000.0)
            duracion = st.slider("Duración estimada (semanas)", 0, 100, 52)
        with col2:
            trabajadores = st.number_input("Tamaño de equipo", value=8, step=1, min_value=1)
            retraso_inicio = st.number_input("Retraso inicial esperado (días)", value=0, min_value=0)
        with col3:
            retraso_final = st.number_input("Retraso final esperado (días)", value=0, min_value=0)
            complejidad = st.selectbox("Complejidad del proyecto", ["baja", "media", "alta"], index=1)
        
        submitted = st.form_submit_button("Generar Predicción y Recomendaciones", type="primary")

    if submitted:
        # Realizar predicción
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
        riesgo = clasificar_nivel_riesgo(pred_defectos, trabajadores, duracion)
        
        # === SECCIÓN 1: RESULTADOS PRINCIPALES ===
        st.markdown("---")
        st.subheader("Resultados de la Predicción")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            st.markdown(
                f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 20px; border-radius: 10px; color: white; text-align: center;'>
                    <h3 style='margin:0;'>Defectos Totales</h3>
                    <h1 style='margin:10px 0; font-size: 3em;'>{pred_defectos:.0f}</h1>
                    <p style='margin:0; opacity: 0.9;'>Defectos esperados durante el proyecto</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col_res2:
            st.markdown(
                f"""
                <div style='background-color: {riesgo["color"]}; 
                            padding: 20px; border-radius: 10px; color: white; text-align: center;'>
                    <h3 style='margin:0;'>Nivel de Riesgo</h3>
                    <h1 style='margin:10px 0; font-size: 3em;'>{riesgo["nivel"]}</h1>
                    <p style='margin:5px 0; opacity: 0.9;'>Tasa: {riesgo["tasa"]:.2f} defectos/persona/semana</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col_res3:
            defectos_por_trabajador = pred_defectos / trabajadores
            st.markdown(
                f"""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 20px; border-radius: 10px; color: white; text-align: center;'>
                    <h3 style='margin:0;'>Por Trabajador</h3>
                    <h1 style='margin:10px 0; font-size: 3em;'>{defectos_por_trabajador:.1f}</h1>
                    <p style='margin:0; opacity: 0.9;'>Defectos promedio por persona</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # === SECCIÓN 2: RECOMENDACIONES INTELIGENTES ===
        st.markdown("---")
        st.subheader("Recomendaciones Inteligentes")
        st.caption("Acciones sugeridas para optimizar la gestión del proyecto y minimizar riesgos")
        
        recomendaciones = generar_recomendaciones(
            pred_defectos, trabajadores, duracion, presupuesto,
            retraso_inicio, retraso_final, complejidad, riesgo
        )
        
        for rec in recomendaciones:
            with st.expander(f"{rec['tipo']}: {rec['titulo']}", expanded=True):
                st.markdown(
                    f"""
                    <div style='background-color: {rec["color"]}15; padding: 15px; border-left: 4px solid {rec["color"]}; border-radius: 5px;'>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown("**Acciones recomendadas:**")
                for accion in rec["acciones"]:
                    st.markdown(f"* {accion}")
                st.markdown("</div>", unsafe_allow_html=True)
        
        # === SECCIÓN 3: CURVA DE RAYLEIGH ===
        st.markdown("---")
        st.subheader("Curva de Acumulación de Defectos (Rayleigh)")
        
        col_chart1, col_chart2 = st.columns([2, 1])
        
        with col_chart1:
            st.line_chart(curva.set_index("Tiempo"), use_container_width=True, height=400)
            st.caption(
                "Esta curva muestra la acumulación esperada de defectos a lo largo del tiempo. "
                "El pico de la pendiente indica el período de mayor detección de defectos."
            )
        
        with col_chart2:
            st.markdown("#### Puntos Clave")
            
            # Encontrar pico de detección (máxima tasa de defectos)
            # El valor 'Tiempo' ya representa semanas directamente
            curva['DefectosSemanales'] = curva['DefectosAcumulados'].diff().fillna(0)
            pico_idx = curva['DefectosSemanales'].idxmax()
            semana_pico = int(curva.iloc[pico_idx]['Tiempo'])
            
            # Encontrar cuándo se alcanza el 50% y 90% de defectos totales
            defectos_totales = curva['DefectosAcumulados'].max()
            idx_50 = (curva['DefectosAcumulados'] >= defectos_totales * 0.5).idxmax()
            idx_90 = (curva['DefectosAcumulados'] >= defectos_totales * 0.9).idxmax()
            semana_50 = int(curva.iloc[idx_50]['Tiempo'])
            semana_90 = int(curva.iloc[idx_90]['Tiempo'])
            
            st.info(f"** Pico de detección:** Semana {semana_pico}")
            st.info(f"** 50% defectos:** Semana {semana_50}")
            st.info(f"** 90% defectos:** Semana {semana_90}")
            
            st.markdown("---")
            st.warning(
                "**Recomendación:** Concentrar máximo esfuerzo de QA "
                f"entre semanas {max(1, semana_pico-1)} y {semana_50+1}"
            )
        
        # === SECCIÓN 4: PLAN DE TESTING ===
        st.markdown("---")
        st.subheader("Plan de Testing Sugerido")
        st.caption("Distribución recomendada de recursos de QA por semana")
        
        plan_testing = generar_plan_testing(pred_defectos, duracion, curva)
        
        # Mostrar tabla sin estilos de color
        st.dataframe(
            plan_testing,
            use_container_width=True,
            height=300
        )
        
        # === SECCIÓN 5: PROYECTOS SIMILARES ===
        st.markdown("---")
        st.subheader("Proyectos Históricos Similares")
        st.caption("Comparación con proyectos que tuvieron características parecidas")
        
        similares = buscar_proyectos_similares(df_proyectos, presupuesto, trabajadores, complejidad)
        
        if len(similares) > 0:
            st.dataframe(similares, use_container_width=True)
            
            # Estadísticas de proyectos similares
            col_sim1, col_sim2, col_sim3 = st.columns(3)
            with col_sim1:
                st.metric("Defectos Promedio Real", f"{similares['TotalErrores'].mean():.0f}")
            with col_sim2:
                st.metric("Retraso Promedio", f"{similares['RetrasoFinalDias'].mean():.1f} días")
            with col_sim3:
                st.metric("Desviación Presupuestal", f"{similares['Desviacion%'].mean():.1f}%")
            
            st.success(
                f"Tu predicción de **{pred_defectos:.0f} defectos** está "
                f"{'dentro del rango' if abs(pred_defectos - similares['TotalErrores'].mean()) < 30 else 'fuera del rango'} "
                f"de proyectos similares (promedio: {similares['TotalErrores'].mean():.0f})"
            )
        else:
            st.info("No se encontraron proyectos históricos con características similares. La predicción se basa únicamente en el modelo general.")
        
        # === SECCIÓN 6: DATOS DETALLADOS ===
        with st.expander("Ver Datos Detallados de la Curva"):
            st.dataframe(curva.head(20), use_container_width=True)
        
        # === SECCIÓN 7: RESUMEN EJECUTIVO ===
        st.markdown("---")
        st.subheader("Resumen Ejecutivo")
        
        # Crear resumen en formato limpio con tema dark
        resumen_html = f"""
        <div style='background-color: #1e1e1e; padding: 25px; border-radius: 10px; border-left: 5px solid {riesgo["color"]}; box-shadow: 0 4px 8px rgba(0,0,0,0.3);'>
            <h3 style='color: {riesgo["color"]}; margin-top: 0;'>
                {riesgo["icono"]} Proyecto Estimado - Riesgo {riesgo["nivel"]}
            </h3>
            <div style='background-color: #2d2d2d; padding: 15px; border-radius: 5px; margin: 15px 0;'>
                <h4 style='margin-top: 0; color: #e0e0e0;'>Parámetros del Proyecto:</h4>
                <table style='width: 100%; border-collapse: collapse;'>
                    <tr style='border-bottom: 1px solid #404040;'>
                        <td style='padding: 8px; font-weight: bold; color: #b0b0b0;'>Defectos Esperados:</td>
                        <td style='padding: 8px; color: #ffffff;'>{pred_defectos:.0f} defectos totales</td>
                    </tr>
                    <tr style='border-bottom: 1px solid #404040;'>
                        <td style='padding: 8px; font-weight: bold; color: #b0b0b0;'>Duración:</td>
                        <td style='padding: 8px; color: #ffffff;'>{duracion} semanas ({duracion/4:.1f} meses)</td>
                    </tr>
                    <tr style='border-bottom: 1px solid #404040;'>
                        <td style='padding: 8px; font-weight: bold; color: #b0b0b0;'>Equipo:</td>
                        <td style='padding: 8px; color: #ffffff;'>{trabajadores} trabajadores</td>
                    </tr>
                    <tr style='border-bottom: 1px solid #404040;'>
                        <td style='padding: 8px; font-weight: bold; color: #b0b0b0;'>Presupuesto:</td>
                        <td style='padding: 8px; color: #ffffff;'>${presupuesto:,.2f}</td>
                    </tr>
                    <tr style='border-bottom: 1px solid #404040;'>
                        <td style='padding: 8px; font-weight: bold; color: #b0b0b0;'>Complejidad:</td>
                        <td style='padding: 8px; color: #ffffff;'>{complejidad.capitalize()}</td>
                    </tr>
                    <tr>
                        <td style='padding: 8px; font-weight: bold; color: #b0b0b0;'>Pico de Defectos:</td>
                        <td style='padding: 8px; color: #ffffff;'>Semana {semana_pico}</td>
                    </tr>
                </table>
            </div>
            <div style='background-color: {riesgo["color"]}25; padding: 15px; border-radius: 5px; border-left: 3px solid {riesgo["color"]};'>
                <h4 style='margin-top: 0; color: #e0e0e0;'>Acción Principal Recomendada:</h4>
                <p style='margin: 0; font-size: 16px; color: #ffffff;'>
                    {recomendaciones[0]['acciones'][0] if recomendaciones else 'Seguir plan de testing sugerido'}
                </p>
            </div>
        </div>
        """
        
        st.markdown(resumen_html, unsafe_allow_html=True)

    if st.button("Reentrenar modelo con datos actualizados"):
        entrenar_modelo.clear()
        st.success("Modelo reentrenado exitosamente con los datos más recientes.")
        st.info("El modelo ahora incorpora todos los proyectos en el sistema para mejorar la precisión.")


def render_metricas_calculadas(filtros: dict):
    """
    Vista que muestra todas las métricas calculadas dinámicamente
    según las especificaciones del proyecto
    """
    st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 25px; border-radius: 12px; margin-bottom: 25px;'>
            <h1 style='color: white; margin: 0; font-size: 2.2em;'>Métricas Calculadas</h1>
            <p style='color: rgba(255,255,255,0.95); margin: 8px 0 0 0; font-size: 1.05em;'>
                Indicadores técnicos: retrasos, presupuesto, costos, eficiencia y productividad
            </p>
            <p style='color: rgba(255,255,255,0.85); margin: 8px 0 0 0; font-size: 0.95em;'>
                <strong>Misión:</strong> Optimizar rendimiento con medición precisa | 
                <strong>Visión:</strong> Mejora continua basada en métricas objetivas
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Obtener dataframe con todas las métricas calculadas
    df_metricas = generar_dataframe_metricas_calculadas()
    stats = obtener_estadisticas_metricas_calculadas()
    
    # Obtener información básica de proyectos para filtros y visualización
    tablas = cargar_tablas_completas()
    
    # Merge simple solo con dim_proyectos para obtener CodigoProyecto
    df_completo = df_metricas.merge(
        tablas["dim_proyectos"][["ID_Proyecto", "CodigoProyecto", "ID_Cliente"]], 
        on="ID_Proyecto", 
        how="left"
    )
    
    # Agregar información de cliente
    df_completo = df_completo.merge(
        tablas["dim_clientes"][["ID_Cliente", "CodigoClienteReal"]], 
        on="ID_Cliente", 
        how="left"
    )
    
    # Agregar información temporal para filtros
    df_tiempo_fin = tablas["dim_tiempo"][["ID_Tiempo", "Anio", "Mes"]].copy()
    df_tiempo_fin = df_tiempo_fin.rename(columns={"Anio": "AnioFin", "Mes": "MesFin"})
    
    df_hechos_fechas = tablas["hechos_proyectos"][["ID_Proyecto", "ID_FechaFin"]]
    df_completo = df_completo.merge(df_hechos_fechas, on="ID_Proyecto", how="left")
    df_completo = df_completo.merge(df_tiempo_fin, left_on="ID_FechaFin", right_on="ID_Tiempo", how="left")
    
    # Verificar si hay datos
    if df_completo.empty:
        st.warning("No hay datos disponibles para las métricas calculadas. Verifica que las tablas del DWH contengan información.")
        return
    
    # Debug: Mostrar columnas disponibles (solo en desarrollo)
    with st.expander("Información de Debug - Columnas Disponibles"):
        st.write(f"**Columnas en df_completo:** {', '.join(list(df_completo.columns))}")
        st.write(f"**Número de registros:** {len(df_completo)}")
        st.dataframe(df_completo.head(3))
    
    # Aplicar filtros
    if filtros.get("anio") and "AnioFin" in df_completo.columns:
        df_completo = df_completo[df_completo["AnioFin"].isin(filtros["anio"])]
    if filtros.get("mes") and "MesFin" in df_completo.columns:
        df_completo = df_completo[df_completo["MesFin"].isin(filtros["mes"])]
    if filtros.get("cliente") and "CodigoClienteReal" in df_completo.columns:
        df_completo = df_completo[df_completo["CodigoClienteReal"].isin(filtros["cliente"])]
    if filtros.get("proyecto") and "CodigoProyecto" in df_completo.columns:
        df_completo = df_completo[df_completo["CodigoProyecto"].isin(filtros["proyecto"])]
    
    # Panel de resumen
    st.subheader("Resumen de Métricas Calculadas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Retraso Inicio Promedio",
            f"{stats['retraso_inicio_promedio']:.1f} días",
            help="RetrasoInicioDias: Diferencia entre fecha inicio planificada y real"
        )
    
    with col2:
        st.metric(
            "Retraso Final Promedio",
            f"{stats['retraso_final_promedio']:.1f} días",
            help="RetrasoFinalDias: Diferencia entre fecha fin planificada y real"
        )
    
    with col3:
        st.metric(
            "Productividad Promedio",
            f"{stats['productividad_promedio']:.1f} hrs/hito",
            help="ProductividadPromedio: Σ(HorasReales) / Cantidad hitos"
        )
    
    with col4:
        st.metric(
            "Costo Real Promedio",
            f"${stats['coste_real_promedio']:,.2f}",
            help="CosteReal: Σ(CostoPorHora × HorasReales) + Σ GastosFinancieros"
        )
    
    # Métricas financieras
    st.subheader("Análisis Financiero")
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.metric(
            "Presupuesto Promedio",
            f"${stats['presupuesto_promedio']:,.2f}",
            help="Presupuesto: ValorTotalContrato del proyecto"
        )
    
    with col_b:
        st.metric(
            "Desviación Presupuestal",
            f"${stats['desviacion_presupuestal_promedio']:,.2f}",
            delta=f"{(stats['desviacion_presupuestal_promedio']/stats['presupuesto_promedio']*100) if stats['presupuesto_promedio'] > 0 else 0:.1f}%",
            help="DesviacionPresupuestal: Presupuesto - CosteReal"
        )
    
    with col_c:
        st.metric(
            "Penalizaciones Totales",
            f"${stats['penalizaciones_total']:,.2f}",
            delta=f"${stats['penalizaciones_promedio']:,.2f} promedio",
            delta_color="inverse",
            help="PenalizacionesMonto: Suma de penalizaciones contractuales"
        )
    
    # Métricas de calidad y eficiencia
    st.subheader("Calidad y Eficiencia de Procesos")
    col_d, col_e, col_f = st.columns(3)
    
    with col_d:
        st.metric(
            "Tareas Retrasadas",
            f"{stats['tareas_retrasadas_porcentaje']*100:.2f}%",
            delta=f"{stats['tareas_retrasadas_porcentaje']*100 - 10:.2f}% vs objetivo 10%",
            delta_color="inverse",
            help="PorcentajeTareasRetrasadas: Tareas con retraso / Total tareas × 100"
        )
    
    with col_e:
        st.metric(
            "Hitos Retrasados",
            f"{stats['hitos_retrasados_porcentaje']*100:.2f}%",
            delta=f"{stats['hitos_retrasados_porcentaje']*100 - 10:.2f}% vs objetivo 10%",
            delta_color="inverse",
            help="PorcentajeHitosRetrasados: Hitos retrasados / Total hitos × 100"
        )
    
    with col_f:
        st.metric(
            "Tasa de Errores",
            f"{stats['tasa_errores_promedio']*100:.2f}%",
            delta=f"{stats['tasa_errores_promedio']*100 - 5:.2f}% vs objetivo 5%",
            delta_color="inverse",
            help="TasaDeErroresEncontrados: Errores / Total tareas × 100"
        )
    
    # Tabla detallada de métricas por proyecto
    st.subheader("Detalle por Proyecto")
    
    # Verificar que tengamos la columna de identificación del proyecto
    col_proyecto = None
    if "CodigoProyecto" in df_completo.columns:
        col_proyecto = "CodigoProyecto"
    elif "ID_Proyecto" in df_completo.columns:
        col_proyecto = "ID_Proyecto"
    else:
        st.error("No se encontró columna de identificación de proyecto")
        return
    
    # Preparar tabla para mostrar con las nuevas métricas
    columnas_mostrar = [col_proyecto, "RetrasoInicioDias", "RetrasoFinalDias", "Presupuesto", 
                        "CosteReal", "DesviacionPresupuestal", "ProductividadPromedio",
                        "TasaDeErroresEncontrados", "TasaDeExitoEnPruebas"]
    
    # Filtrar solo columnas que existan en el dataframe
    columnas_existentes = [col for col in columnas_mostrar if col in df_completo.columns]
    
    if not columnas_existentes:
        st.warning("No se encontraron las columnas esperadas en los datos")
        return
    
    tabla_display = df_completo[columnas_existentes].copy()
    
    # Preparar diccionario de renombrado dinámicamente
    rename_dict = {
        col_proyecto: "Proyecto",
        "RetrasoInicioDias": "Retraso Inicio (días)",
        "RetrasoFinalDias": "Retraso Final (días)",
        "Presupuesto": "Presupuesto ($)",
        "CosteReal": "Costo Real ($)",
        "DesviacionPresupuestal": "Desviación ($)",
        "ProductividadPromedio": "Productividad (hrs/hito)",
        "TasaDeErroresEncontrados": "Tasa Errores (%)",
        "TasaDeExitoEnPruebas": "Éxito Pruebas (%)"
    }
    
    # Filtrar solo las claves que existan en las columnas
    rename_dict_filtrado = {k: v for k, v in rename_dict.items() if k in tabla_display.columns}
    tabla_display = tabla_display.rename(columns=rename_dict_filtrado)
    
    # Formatear columnas numéricas para mejor visualización
    if "Presupuesto ($)" in tabla_display.columns:
        tabla_display["Presupuesto ($)"] = tabla_display["Presupuesto ($)"].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "N/A")
    if "Costo Real ($)" in tabla_display.columns:
        tabla_display["Costo Real ($)"] = tabla_display["Costo Real ($)"].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "N/A")
    if "Desviación ($)" in tabla_display.columns:
        tabla_display["Desviación ($)"] = tabla_display["Desviación ($)"].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "N/A")
    if "Tasa Errores (%)" in tabla_display.columns:
        tabla_display["Tasa Errores (%)"] = tabla_display["Tasa Errores (%)"].apply(lambda x: f"{x*100:.2f}%" if pd.notna(x) else "N/A")
    if "Éxito Pruebas (%)" in tabla_display.columns:
        tabla_display["Éxito Pruebas (%)"] = tabla_display["Éxito Pruebas (%)"].apply(lambda x: f"{x*100:.2f}%" if pd.notna(x) else "N/A")
    
    st.dataframe(tabla_display, use_container_width=True, height=400)
    
    # Gráficos de visualización
    st.subheader("Visualizaciones de Métricas")
    
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        st.markdown("#### Retrasos de Inicio por Proyecto")
        if "RetrasoInicioDias" in df_completo.columns and col_proyecto in df_completo.columns:
            chart_data = df_completo[[col_proyecto, "RetrasoInicioDias"]].set_index(col_proyecto).head(15)
            st.bar_chart(chart_data, use_container_width=True)
            st.caption("Días de retraso entre fecha inicio planificada y real")
        else:
            st.info("Datos no disponibles para esta visualización")
    
    with col_viz2:
        st.markdown("#### Productividad por Proyecto")
        if "ProductividadPromedio" in df_completo.columns and col_proyecto in df_completo.columns:
            chart_data2 = df_completo[[col_proyecto, "ProductividadPromedio"]].set_index(col_proyecto).head(15)
            st.bar_chart(chart_data2, use_container_width=True)
            st.caption("Horas promedio por hito alcanzado")
        else:
            st.info("Datos no disponibles para esta visualización")
    
    # Desglose financiero
    st.subheader("Análisis Financiero por Proyecto")
    
    col_fin1, col_fin2 = st.columns(2)
    
    with col_fin1:
        st.markdown("#### Presupuesto vs Costo Real")
        if all(col in df_completo.columns for col in [col_proyecto, "Presupuesto", "CosteReal"]):
            comparacion_financiera = df_completo[[col_proyecto, "Presupuesto", "CosteReal"]].set_index(col_proyecto).head(10)
            st.bar_chart(comparacion_financiera, use_container_width=True)
            st.caption("Comparación entre presupuesto planificado y costo real ejecutado")
        else:
            st.info("Datos no disponibles para esta visualización")
    
    with col_fin2:
        st.markdown("#### Desviación Presupuestal")
        if all(col in df_completo.columns for col in [col_proyecto, "DesviacionPresupuestal"]):
            desviaciones = df_completo[[col_proyecto, "DesviacionPresupuestal"]].set_index(col_proyecto).head(10)
            st.bar_chart(desviaciones, use_container_width=True, color="#ff5858")
            st.caption("Desviación = Presupuesto - CosteReal (valores negativos indican sobrecosto)")
        else:
            st.info("Datos no disponibles para esta visualización")


def render_okrs(df_proyectos: pd.DataFrame, df_asignaciones: pd.DataFrame, filtros: dict):
    """
    Vista que muestra los OKRs (Objectives and Key Results) con progreso y estado
    """
    # Calcular KPIs
    kpis = get_kpis(df_proyectos, df_asignaciones, filtros)
    
    # Calcular progreso de OKRs
    okrs_progreso = calcular_todos_okrs(kpis)
    
    # Header
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 15px; margin-bottom: 30px;'>
            <h1 style='color: white; margin: 0; text-align: center; font-size: 2.5em;'>
                OKRs - Objectives and Key Results
            </h1>
            <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 10px 0 0 0; font-size: 1.1em;'>
                Objetivos estratégicos y resultados clave medibles
            </p>
            <p style='color: rgba(255,255,255,0.85); text-align: center; margin: 8px 0 0 0; font-size: 0.95em;'>
                 <strong>Misión:</strong> Optimizar procesos con objetivos claros | 
                 <strong>Visión:</strong> Excelencia sostenible mediante resultados medibles
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Resumen global ANTES de mostrar cada OKR
    st.markdown("---")
    st.subheader("Resumen Global de OKRs")
    
    col1, col2, col3, col4 = st.columns(4)
    
    okr_configs = [
        ("O1_Excelencia_Financiera", "#11998e", "#38ef7d"),
        ("O2_Satisfaccion_Cliente", "#2980b9", "#6dd5fa"),
        ("O3_Procesos_Eficientes", "#f857a6", "#ff5858"),
        ("O4_Equipos_Alto_Desempeño", "#fa709a", "#fee140")
    ]
    
    for idx, (okr_key, _, _) in enumerate(okr_configs):
        okr_data = okrs_progreso[okr_key]
        progreso = okr_data["progreso_general"]
        
        if progreso >= 85:
            estado = "EXCELENTE"
            color_fondo = "#d1fae5"
            color_texto = "#065f46"
        elif progreso >= 70:
            estado = "EN CAMINO"
            color_fondo = "#fef3c7"
            color_texto = "#92400e"
        else:
            estado = "REQUIERE ATENCIÓN"
            color_fondo = "#fee2e2"
            color_texto = "#991b1b"
        
        with [col1, col2, col3, col4][idx]:
            st.markdown(f"""
                <div style='background: {color_fondo}; padding: 15px; border-radius: 8px; text-align: center;'>
                    <div style='font-size: 2em; font-weight: bold; color: {color_texto};'>
                        {progreso:.0f}%
                    </div>
                    <div style='font-size: 0.9em; color: {color_texto}; margin-top: 5px;'>
                        {estado}
                    </div>
                    <div style='font-size: 0.8em; color: #666; margin-top: 8px;'>
                        {okr_data["objetivo"][:30]}...
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Mostrar cada OKR con detalle
    
    for okr_key, color1, color2 in okr_configs:
        okr_data = okrs_progreso[okr_key]
        progreso = okr_data["progreso_general"]
        
        # Determinar color de progreso
        if progreso >= 85:
            progreso_color = "#10b981"  # Verde
            estado_emoji = "●"
        elif progreso >= 70:
            progreso_color = "#f59e0b"  # Amarillo
            estado_emoji = "●"
        else:
            progreso_color = "#ef4444"  # Rojo
            estado_emoji = "●"
        
        # Header del OKR
        st.markdown(f"""
            <div style='background: linear-gradient(to right, {color1}, {color2}); 
                        padding: 15px 20px; border-radius: 10px; margin: 20px 0 15px 0;'>
                <h2 style='color: white; margin: 0; font-size: 1.6em;'>{okr_data["objetivo"]}</h2>
                <p style='color: rgba(255,255,255,0.95); margin: 5px 0 0 0; font-size: 0.95em;'>
                    {okr_data["descripcion"]}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Progreso general
        st.markdown(f"""
            <div style='background: white; padding: 15px; border-radius: 8px; margin-bottom: 15px;
                        border: 2px solid {progreso_color};'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span style='font-size: 1.1em; font-weight: 600;'>
                        {estado_emoji} Progreso General
                    </span>
                    <span style='font-size: 1.3em; font-weight: bold; color: {progreso_color};'>
                        {progreso:.1f}%
                    </span>
                </div>
                <div style='background: #e5e7eb; height: 20px; border-radius: 10px; margin-top: 10px; overflow: hidden;'>
                    <div style='background: {progreso_color}; height: 100%; width: {progreso}%; 
                                transition: width 0.3s ease;'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Key Results
        st.markdown("**Key Results:**")
        
        cols = st.columns(len(okr_data["key_results"]))
        
        for idx, kr_data in enumerate(okr_data["key_results"]):
            with cols[idx]:
                kr_progreso = kr_data["progreso"]
                
                # Color del KR
                if kr_progreso >= 90:
                    kr_color = "#10b981"
                    kr_emoji = "✓"
                elif kr_progreso >= 75:
                    kr_color = "#3b82f6"
                    kr_emoji = "●"
                elif kr_progreso >= 50:
                    kr_color = "#f59e0b"
                    kr_emoji = "!"
                else:
                    kr_color = "#ef4444"
                    kr_emoji = "✗"
                
                st.markdown(f"""
                    <div style='background: rgba(0,0,0,0.02); padding: 12px; border-radius: 8px; 
                                border-left: 4px solid {kr_color}; margin-bottom: 10px;'>
                        <div style='font-weight: 600; margin-bottom: 5px;'>
                            {kr_emoji} {kr_data["kr"]}
                        </div>
                        <div style='font-size: 0.85em; color: #666; margin-bottom: 8px;'>
                            {kr_data["descripcion"]}
                        </div>
                        <div style='display: flex; justify-content: space-between; font-size: 0.85em;'>
                            <span>Actual: <strong>{kr_data["metrica_valor"]:.2f}</strong></span>
                            <span>Target: <strong>{kr_data["target"]:.2f}</strong></span>
                        </div>
                        <div style='background: #e5e7eb; height: 8px; border-radius: 4px; margin-top: 8px; overflow: hidden;'>
                            <div style='background: {kr_color}; height: 100%; width: {kr_progreso}%;'></div>
                        </div>
                        <div style='text-align: center; margin-top: 5px; font-weight: 600; color: {kr_color};'>
                            {kr_progreso:.1f}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Resumen global
    st.markdown("---")
    st.subheader("Resumen Global de OKRs")
    
    col1, col2, col3, col4 = st.columns(4)
    
    for idx, (okr_key, _, _) in enumerate(okr_configs):
        okr_data = okrs_progreso[okr_key]
        progreso = okr_data["progreso_general"]
        
        if progreso >= 85:
            estado = "EXCELENTE"
            color_fondo = "#d1fae5"
            color_texto = "#065f46"
        elif progreso >= 70:
            estado = "EN CAMINO"
            color_fondo = "#fef3c7"
            color_texto = "#92400e"
        else:
            estado = "REQUIERE ATENCIÓN"
            color_fondo = "#fee2e2"
            color_texto = "#991b1b"
        
        with [col1, col2, col3, col4][idx]:
            st.markdown(f"""
                <div style='background: {color_fondo}; padding: 15px; border-radius: 8px; text-align: center;'>
                    <div style='font-size: 2em; font-weight: bold; color: {color_texto};'>
                        {progreso:.0f}%
                    </div>
                    <div style='font-size: 0.9em; color: {color_texto}; margin-top: 5px;'>
                        {estado}
                    </div>
                    <div style='font-size: 0.8em; color: #666; margin-top: 8px;'>
                        {okr_data["objetivo"][:30]}...
                    </div>
                </div>
            """, unsafe_allow_html=True)
