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

