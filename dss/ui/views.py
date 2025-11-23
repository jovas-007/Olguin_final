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
from dss.ui.components import mostrar_tarjeta_kpi
from dss.metricas_calculadas import (
    generar_dataframe_metricas_calculadas,
    obtener_estadisticas_metricas_calculadas,
    cargar_tablas_completas
)


def render_scorecard(df_proyectos: pd.DataFrame, df_asignaciones: pd.DataFrame, filtros: dict):
    kpis = get_kpis(df_proyectos, df_asignaciones, filtros)
    vistas = build_olap_views(df_proyectos, df_asignaciones, filtros)

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
        )
    with col_fin3:
        mostrar_tarjeta_kpi(
            "Penalizaciones sobre presupuesto",
            kpis["penalizaciones_sobre_presupuesto"],
            KPI_TARGETS["penalizaciones_sobre_presupuesto"],
            "Minimiza riesgos económicos y refuerza acuerdos de calidad.",
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # PERSPECTIVA DEL CLIENTE
    st.markdown("""
        <div style='background: linear-gradient(to right, #2980b9, #6dd5fa); 
                    padding: 15px 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0; font-size: 1.8em;'>Perspectiva del Cliente</h2>
            <p style='color: rgba(255,255,255,0.95); margin: 5px 0 0 0;'>
                Cumplimiento de compromisos, confianza y fidelización
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
            "Proyectos cancelados",
            1 - kpis["proyectos_cancelados"],
            1 - KPI_TARGETS["proyectos_cancelados"],
            "Gestión de riesgos temprana evita cancelaciones y refuerza la reputación.",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # PERSPECTIVA DE PROCESOS INTERNOS
    st.markdown("""
        <div style='background: linear-gradient(to right, #f857a6, #ff5858); 
                    padding: 15px 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0; font-size: 1.8em;'>Perspectiva de Procesos Internos</h2>
            <p style='color: rgba(255,255,255,0.95); margin: 5px 0 0 0;'>
                Operación ágil, trazabilidad y calidad del producto
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_proc1, col_proc2, col_proc3 = st.columns(3)
    with col_proc1:
        mostrar_tarjeta_kpi(
            "Porcentaje de tareas retrasadas",
            1 - kpis["porcentaje_tareas_retrasadas"],
            1 - KPI_TARGETS["porcentaje_tareas_retrasadas"],
            "Menos retrasos implica operación ágil y trazable.",
        )
    with col_proc2:
        mostrar_tarjeta_kpi(
            "Porcentaje de hitos retrasados",
            1 - kpis["porcentaje_hitos_retrasados"],
            1 - KPI_TARGETS["porcentaje_hitos_retrasados"],
            "Entrega disciplinada de hitos acelera valor al cliente.",
        )
    with col_proc3:
        mostrar_tarjeta_kpi(
            "Tasa de errores encontrados",
            1 - kpis["tasa_errores"],
            1 - KPI_TARGETS["tasa_errores"],
            "Calidad del producto mejora satisfacción y reduce reprocesos.",
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # PERSPECTIVA DE APRENDIZAJE E INNOVACIÓN
    st.markdown("""
        <div style='background: linear-gradient(to right, #fa709a, #fee140); 
                    padding: 15px 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0; font-size: 1.8em;'>Perspectiva de Aprendizaje e Innovación</h2>
            <p style='color: rgba(255,255,255,0.95); margin: 5px 0 0 0;'>
                Colaboración interdisciplinaria, mejora continua y escalabilidad
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

    st.markdown("---")
    
    # VISUALIZACIONES CLAVE con diseño mejorado
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
            # Verificar que la columna Fecha existe y tiene valores
            if "Fecha" in vistas["proyectos_a_tiempo"].columns and "A_Tiempo" in vistas["proyectos_a_tiempo"].columns:
                chart_data = vistas["proyectos_a_tiempo"].set_index("Fecha")[["A_Tiempo"]]
                st.line_chart(
                    chart_data,
                    use_container_width=True,
                    height=400
                )
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

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tercera fila - Visualización única más grande
    st.markdown("""
        <div style='background: linear-gradient(to right, #8e2de2, #4a00e0); 
                    padding: 12px 18px; border-radius: 8px; margin-bottom: 12px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h4 style='margin: 0; color: white; font-weight: 600;'>Distribución CAPEX/OPEX por Categoría</h4>
            <p style='margin: 4px 0 0 0; color: rgba(255,255,255,0.9); font-size: 0.9em;'>
                Equilibrio de inversiones de capital vs operativas
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.bar_chart(
        vistas["capex_opex"].set_index("Categoria")[["ProporcionCAPEX_OPEX"]],
        use_container_width=True,
        height=350
    )
    st.caption("Distribución estratégica de gastos para equilibrar inversiones a largo plazo (CAPEX) y operativas (OPEX).")




def render_detalle(df_proyectos: pd.DataFrame, df_asignaciones: pd.DataFrame, filtros: dict):
    vistas = build_olap_views(df_proyectos, df_asignaciones, filtros)
    detalle = get_detail_table(df_proyectos, filtros)

    # Header principal
    st.header("Análisis Detallado de Proyectos")
    st.caption("Vista operativa completa con desglose de métricas clave por proyecto")
    
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
    st.header("Predicción de Defectos con IA")
    st.caption(
        "Sistema de predicción basado en Machine Learning y distribución de Rayleigh. "
        "Optimiza procesos con tecnología para decisiones basadas en datos."
    )

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

    with st.form("prediccion_form"):
        st.subheader("Parámetros del Proyecto")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            presupuesto = st.number_input("Presupuesto estimado ($)", value=400000.0, step=5000.0)
            duracion = st.slider("Duración estimada (semanas)", 4, 52, 16)
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
            
            # Encontrar pico de detección
            curva['DefectosSemanales'] = curva['DefectosAcumulados'].diff().fillna(0)
            pico_idx = curva['DefectosSemanales'].idxmax()
            semana_pico = int(curva.iloc[pico_idx]['Tiempo'] / 7)
            
            st.info(f"** Pico de detección:** Semana {semana_pico}")
            st.info(f"** 50% defectos:** Semana {int(len(curva) * 0.4 / 7)}")
            st.info(f"** 90% defectos:** Semana {int(len(curva) * 0.8 / 7)}")
            
            st.markdown("---")
            st.warning(
                "**Recomendación:** Concentrar máximo esfuerzo de QA "
                f"entre semanas {max(1, semana_pico-2)} y {semana_pico+2}"
            )
        
        # === SECCIÓN 4: PLAN DE TESTING ===
        st.markdown("---")
        st.subheader("Plan de Testing Sugerido")
        st.caption("Distribución recomendada de recursos de QA por semana")
        
        plan_testing = generar_plan_testing(pred_defectos, duracion, curva)
        
        # Mostrar tabla con estilo
        st.dataframe(
            plan_testing.style.applymap(
                lambda x: 'background-color: #ffebee' if x == "Alto" 
                else 'background-color: #fff9c4' if x == "Medio" 
                else 'background-color: #e8f5e9' if x == "Bajo" 
                else '',
                subset=['Esfuerzo QA']
            ),
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
    st.header("Métricas Calculadas Dinámicamente")
    st.caption("Métricas calculadas en tiempo real desde las tablas de dimensiones y hechos")
    
    # Obtener dataframe con todas las métricas calculadas
    df_metricas = generar_dataframe_metricas_calculadas()
    stats = obtener_estadisticas_metricas_calculadas()
    
    # Merge con datos de proyectos para filtrar
    tablas = cargar_tablas_completas()
    df_proyectos_info = tablas["hechos_proyectos"].merge(
        tablas["dim_proyectos"], on="ID_Proyecto"
    ).merge(
        tablas["dim_clientes"], on="ID_Cliente"
    ).merge(
        tablas["dim_tiempo"], left_on="ID_FechaFin", right_on="ID_Tiempo"
    )
    
    df_completo = df_metricas.merge(df_proyectos_info, on="ID_Proyecto")
    
    # Aplicar filtros
    if filtros.get("anio"):
        df_completo = df_completo[df_completo["Anio"].isin(filtros["anio"])]
    if filtros.get("mes"):
        df_completo = df_completo[df_completo["Mes"].isin(filtros["mes"])]
    if filtros.get("cliente"):
        df_completo = df_completo[df_completo["CodigoClienteReal"].isin(filtros["cliente"])]
    if filtros.get("proyecto"):
        df_completo = df_completo[df_completo["CodigoProyecto"].isin(filtros["proyecto"])]
    
    # Panel de resumen
    st.subheader("Resumen de Métricas Calculadas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Duración Promedio",
            f"{stats['duracion_promedio_dias']:.1f} días",
            help="DuracionRealDias: Número de días reales de ejecución del proyecto"
        )
    
    with col2:
        st.metric(
            "Defectos Encontrados",
            f"{stats['defectos_total']:.0f} total",
            delta=f"{stats['defectos_promedio']:.1f} promedio",
            help="NumeroDefectosEncontrados: Total de defectos o errores identificados (pruebas fallidas)"
        )
    
    with col3:
        st.metric(
            "Productividad Calculada",
            f"{stats['productividad_calculada']:.2f}",
            help="ProductividadPromedio: DuracionReal / No_empleados"
        )
    
    with col4:
        st.metric(
            "Costo Real Promedio",
            f"${stats['costo_real_promedio']:,.2f}",
            help="CostoReal: Σ(CostoPorHora × HorasReales) + Σ GastosFinancieros"
        )
    
    # Métricas de retrasos
    st.subheader("Análisis de Retrasos")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.metric(
            "Tareas Retrasadas (Calculado)",
            f"{stats['tareas_retrasadas_calculada']*100:.2f}%",
            delta=f"{stats['tareas_retrasadas_calculada']*100 - 10:.2f}% vs objetivo 10%",
            delta_color="inverse",
            help="PorcentajeTareasRetrasadas: (COUNT(TareasRetrasadas) / COUNT(TareasTotales)) × 100"
        )
    
    with col_b:
        st.metric(
            "Hitos Retrasados (Calculado)",
            f"{stats['hitos_retrasados_calculada']*100:.2f}%",
            delta=f"{stats['hitos_retrasados_calculada']*100 - 10:.2f}% vs objetivo 10%",
            delta_color="inverse",
            help="PorcentajeHitosRetrasados: (COUNT(HitosRetrasados) / COUNT(HitosTotales)) × 100"
        )
    
    # Tabla detallada de métricas por proyecto
    st.subheader("Detalle por Proyecto")
    
    # Preparar tabla para mostrar
    tabla_display = df_completo[[
        "CodigoProyecto",
        "DuracionRealDias",
        "NumeroDefectosEncontrados",
        "ProductividadPromedio_Calculada",
        "PorcentajeTareasRetrasadas_Calculada",
        "PorcentajeHitosRetrasados_Calculada",
        "CostoReal_Total_Calculado"
    ]].copy()
    
    tabla_display = tabla_display.rename(columns={
        "CodigoProyecto": "Proyecto",
        "DuracionRealDias": "Duración (días)",
        "NumeroDefectosEncontrados": "Defectos",
        "ProductividadPromedio_Calculada": "Productividad",
        "PorcentajeTareasRetrasadas_Calculada": "% Tareas Retrasadas",
        "PorcentajeHitosRetrasados_Calculada": "% Hitos Retrasados",
        "CostoReal_Total_Calculado": "Costo Real Total"
    })
    
    # Formatear columnas
    tabla_display["% Tareas Retrasadas"] = tabla_display["% Tareas Retrasadas"].apply(lambda x: f"{x:.2f}%")
    tabla_display["% Hitos Retrasados"] = tabla_display["% Hitos Retrasados"].apply(lambda x: f"{x:.2f}%")
    tabla_display["Costo Real Total"] = tabla_display["Costo Real Total"].apply(lambda x: f"${x:,.2f}")
    tabla_display["Productividad"] = tabla_display["Productividad"].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(tabla_display, use_container_width=True)
    
    # Comparación: Métricas Precalculadas vs Calculadas
    st.subheader("Comparación: Precalculadas vs Calculadas")
    st.info(
        "Esta sección compara las métricas que vienen precalculadas en los datos "
        "con las calculadas dinámicamente según las fórmulas especificadas."
    )
    
    col_comp1, col_comp2 = st.columns(2)
    
    with col_comp1:
        st.markdown("#### Productividad")
        comparacion_prod = df_completo[[
            "CodigoProyecto",
            "ProductividadPromedio",
            "ProductividadPromedio_Calculada"
        ]].head(10)
        st.dataframe(comparacion_prod, use_container_width=True)
    
    with col_comp2:
        st.markdown("#### Tareas Retrasadas (%)")
        comparacion_tareas = df_completo[[
            "CodigoProyecto",
            "PorcentajeTareasRetrasadas",
            "PorcentajeTareasRetrasadas_Calculada"
        ]].head(10)
        st.dataframe(comparacion_tareas, use_container_width=True)
    
    # Gráficos
    st.subheader("Visualizaciones")
    
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        st.markdown("#### Defectos por Proyecto")
        chart_data = df_completo[["CodigoProyecto", "NumeroDefectosEncontrados"]].set_index("CodigoProyecto")
        st.bar_chart(chart_data, use_container_width=True)
    
    with col_viz2:
        st.markdown("#### Duración Real (días)")
        chart_data2 = df_completo[["CodigoProyecto", "DuracionRealDias"]].set_index("CodigoProyecto")
        st.bar_chart(chart_data2, use_container_width=True)
    
    # Desglose de costos
    st.subheader("Desglose de Costos Reales")
    costos_desglose = df_completo[[
        "CodigoProyecto",
        "CostoReal_Horas",
        "CostoReal_Gastos"
    ]].set_index("CodigoProyecto")
    
    costos_desglose = costos_desglose.rename(columns={
        "CostoReal_Horas": "Costo Horas Trabajadas",
        "CostoReal_Gastos": "Gastos Financieros"
    })
    
    st.bar_chart(costos_desglose, use_container_width=True)
    st.caption(
        "CostoReal = Σ(CostoPorHoraEmpleado × HorasReales) + Σ GastosFinancieros. "
        "Muestra la composición del costo real entre horas trabajadas y gastos financieros."
    )

