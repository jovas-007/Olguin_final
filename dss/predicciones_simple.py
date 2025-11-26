"""
Módulo de predicciones simples para recomendaciones en Balanced Scorecard
Usa análisis de tendencias y promedios para generar predicciones útiles
"""

import pandas as pd
import numpy as np
from typing import Dict, List


def predecir_riesgo_financiero(kpis: Dict, vistas: Dict) -> Dict:
    """
    Predice riesgo financiero basado en KPIs actuales
    Retorna nivel de riesgo y recomendaciones
    """
    cumplimiento = kpis.get("cumplimiento_presupuesto", 1.0)
    desviacion = abs(kpis.get("desviacion_presupuestal", 0))
    penalizaciones = kpis.get("penalizaciones_sobre_presupuesto", 0)
    
    # Calcular score de riesgo (0-100, menor es mejor)
    riesgo_score = 0
    
    if cumplimiento < 0.85:
        riesgo_score += 35
    elif cumplimiento < 0.95:
        riesgo_score += 15
    
    # Desviación presupuestal ahora está normalizada (0-1)
    if desviacion > 0.20:  # Más de 20% de desviación
        riesgo_score += 40
    elif desviacion > 0.10:  # Entre 10-20%
        riesgo_score += 25
    elif desviacion > 0.05:  # Entre 5-10%
        riesgo_score += 10
    
    if penalizaciones > 0.05:  # Más de 5%
        riesgo_score += 25
    elif penalizaciones > 0.02:  # Entre 2-5%
        riesgo_score += 10
    
    # Determinar nivel de riesgo
    if riesgo_score >= 50:
        nivel = "ALTO"
        color = "🔴"
    elif riesgo_score >= 25:
        nivel = "MEDIO"
        color = "🟡"
    else:
        nivel = "BAJO"
        color = "🟢"
    
    # Generar recomendaciones
    recomendaciones = []
    
    if cumplimiento < 0.95:
        recomendaciones.append("Revisar procesos de estimación de presupuestos")
        if cumplimiento < 0.85:
            recomendaciones.append("Implementar controles de costos más estrictos urgentemente")
    
    if desviacion > 0.20:
        recomendaciones.append("CRÍTICO: Desviación presupuestal superior al 20%")
        recomendaciones.append("Análisis inmediato de causas raíz de sobrecostos")
        recomendaciones.append("Plan de acción correctivo en próximas 48 horas")
    elif desviacion > 0.10:
        recomendaciones.append("Analizar causas de desviación presupuestal (>10%)")
        recomendaciones.append("Establecer alertas tempranas de sobrecostos")
        recomendaciones.append("Revisar scope creep y change requests")
    elif desviacion > 0.05:
        recomendaciones.append("Monitorear desviación presupuestal")
        recomendaciones.append("Reforzar seguimiento de gastos")
    
    if penalizaciones > 0.02:
        recomendaciones.append("Mejorar cumplimiento de SLAs contractuales")
        recomendaciones.append("Reforzar gestión de expectativas con clientes")
    
    if not recomendaciones:
        recomendaciones.append("Mantener buenas prácticas actuales")
        recomendaciones.append("Continuar monitoreo de indicadores financieros")
    
    return {
        "nivel": nivel,
        "color": color,
        "score": riesgo_score,
        "recomendaciones": recomendaciones
    }


def predecir_satisfaccion_cliente(kpis: Dict, vistas: Dict) -> Dict:
    """
    Predice satisfacción del cliente basado en entregas y cancelaciones
    """
    proyectos_a_tiempo = kpis.get("proyectos_a_tiempo", 0)
    proyectos_cancelados = kpis.get("proyectos_cancelados", 0)
    
    # Score de satisfacción (0-100)
    # Ajustado para objetivo de 30% cancelados
    satisfaccion_score = proyectos_a_tiempo * 60 + (1 - proyectos_cancelados) * 40
    
    if satisfaccion_score >= 85:
        nivel = "EXCELENTE"
        color = "🟢"
    elif satisfaccion_score >= 70:
        nivel = "BUENO"
        color = "🟡"
    else:
        nivel = "REQUIERE ATENCIÓN"
        color = "🔴"
    
    recomendaciones = []
    
    if proyectos_a_tiempo < 0.85:
        recomendaciones.append("Mejorar planificación de cronogramas")
        recomendaciones.append("Implementar metodologías ágiles para mayor flexibilidad")
        recomendaciones.append("Realizar revisiones de hitos más frecuentes")
    
    if proyectos_cancelados > 0.30:
        recomendaciones.append("CRÍTICO: Más del 30% de proyectos cancelados")
        recomendaciones.append("Revisar proceso de selección y aprobación de proyectos")
        recomendaciones.append("Fortalecer análisis de viabilidad y ROI pre-proyecto")
    elif proyectos_cancelados > 0.20:
        recomendaciones.append("Tasa de cancelación elevada (>20%)")
        recomendaciones.append("Mejorar comunicación con stakeholders")
        recomendaciones.append("Establecer checkpoints de go/no-go tempranos")
    elif proyectos_cancelados > 0.10:
        recomendaciones.append("Monitorear tasa de cancelación")
        recomendaciones.append("Reforzar gestión de expectativas desde inicio")
    
    if not recomendaciones:
        recomendaciones.append("Excelente gestión de entregas")
        recomendaciones.append("Mantener comunicación proactiva con clientes")
    
    return {
        "nivel": nivel,
        "color": color,
        "score": satisfaccion_score,
        "recomendaciones": recomendaciones
    }


def predecir_eficiencia_procesos(kpis: Dict, vistas: Dict) -> Dict:
    """
    Predice eficiencia de procesos internos
    """
    tareas_retrasadas = kpis.get("porcentaje_tareas_retrasadas", 0)
    hitos_retrasados = kpis.get("porcentaje_hitos_retrasados", 0)
    tasa_errores = kpis.get("tasa_errores", 0)
    
    # Normalizar si vienen en escala 0-100 en lugar de 0-1
    if tareas_retrasadas > 1:
        tareas_retrasadas = tareas_retrasadas / 100
    if hitos_retrasados > 1:
        hitos_retrasados = hitos_retrasados / 100
    if tasa_errores > 1:
        tasa_errores = tasa_errores / 100
    
    # Score de eficiencia (0-100, mayor es mejor)
    eficiencia_score = (
        (1 - tareas_retrasadas) * 33.33 +
        (1 - hitos_retrasados) * 33.33 +
        (1 - tasa_errores) * 33.33
    )
    
    if eficiencia_score >= 85:
        nivel = "ÓPTIMO"
        color = "🟢"
    elif eficiencia_score >= 70:
        nivel = "ACEPTABLE"
        color = "🟡"
    else:
        nivel = "CRÍTICO"
        color = "🔴"
    
    recomendaciones = []
    
    if tareas_retrasadas > 0.15:
        recomendaciones.append("Redistribuir carga de trabajo entre equipo")
        recomendaciones.append("Revisar estimaciones de tareas")
        recomendaciones.append("Implementar dailies para seguimiento continuo")
    
    if hitos_retrasados > 0.15:
        recomendaciones.append("Mejorar definición de hitos críticos")
        recomendaciones.append("Establecer buffers en planificación")
    
    if tasa_errores > 0.07:
        recomendaciones.append("Reforzar code reviews y pair programming")
        recomendaciones.append("Incrementar cobertura de pruebas automatizadas")
        recomendaciones.append("Capacitar equipo en mejores prácticas")
    
    if not recomendaciones:
        recomendaciones.append("Procesos funcionando de manera óptima")
        recomendaciones.append("Documentar lecciones aprendidas")
    
    return {
        "nivel": nivel,
        "color": color,
        "score": eficiencia_score,
        "recomendaciones": recomendaciones
    }


def predecir_desarrollo_equipo(kpis: Dict, vistas: Dict) -> Dict:
    """
    Predice necesidades de desarrollo del equipo
    """
    productividad = kpis.get("productividad_promedio", 0)
    tasa_exito_pruebas = kpis.get("tasa_exito_pruebas", 0)
    horas_relacion = kpis.get("horas_relacion", 1.0)
    
    # Score de capacidad del equipo (0-100)
    # Normalizar productividad (target: 400 hrs/hito, excelente: 500+)
    productividad_norm = min(productividad / 500, 1.0) if productividad > 0 else 0
    precision_estimacion = max(0, 1 - abs(horas_relacion - 1.0))
    
    capacidad_score = (
        productividad_norm * 40 +
        tasa_exito_pruebas * 40 +
        precision_estimacion * 20
    )
    
    if capacidad_score >= 85:
        nivel = "ALTO DESEMPEÑO"
        color = "🟢"
    elif capacidad_score >= 70:
        nivel = "COMPETENTE"
        color = "🟡"
    else:
        nivel = "NECESITA DESARROLLO"
        color = "🔴"
    
    recomendaciones = []
    
    if productividad < 300:
        recomendaciones.append("Identificar obstáculos que reducen productividad")
        recomendaciones.append("Considerar herramientas de automatización")
        recomendaciones.append("Evaluar distribución de skills en el equipo")
    
    if tasa_exito_pruebas < 0.85:
        recomendaciones.append("Capacitar en estrategias de testing")
        recomendaciones.append("Implementar TDD (Test-Driven Development)")
        recomendaciones.append("Mejorar ambiente de QA")
    
    if abs(horas_relacion - 1.0) > 0.15:
        recomendaciones.append("Mejorar técnicas de estimación (Planning Poker)")
        recomendaciones.append("Analizar velocity histórico del equipo")
        recomendaciones.append("Considerar factores de contingencia más realistas")
    
    if not recomendaciones:
        recomendaciones.append("Equipo de alto desempeño")
        recomendaciones.append("Fomentar mentoría interna")
        recomendaciones.append("Compartir mejores prácticas con otros equipos")
    
    return {
        "nivel": nivel,
        "color": color,
        "score": capacidad_score,
        "recomendaciones": recomendaciones
    }


def generar_todas_predicciones(kpis: Dict, vistas: Dict) -> Dict:
    """
    Genera todas las predicciones para las 4 perspectivas del BSC
    """
    return {
        "financiera": predecir_riesgo_financiero(kpis, vistas),
        "cliente": predecir_satisfaccion_cliente(kpis, vistas),
        "procesos": predecir_eficiencia_procesos(kpis, vistas),
        "aprendizaje": predecir_desarrollo_equipo(kpis, vistas)
    }
