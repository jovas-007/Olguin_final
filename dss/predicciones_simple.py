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
        riesgo_score += 40
    elif cumplimiento < 0.90:
        riesgo_score += 20
    
    if desviacion > 0.10:
        riesgo_score += 30
    elif desviacion > 0.05:
        riesgo_score += 15
    
    if penalizaciones > 0.05:
        riesgo_score += 30
    elif penalizaciones > 0.02:
        riesgo_score += 15
    
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
    
    if cumplimiento < 0.90:
        recomendaciones.append("Revisar procesos de estimación de presupuestos")
        recomendaciones.append("Implementar controles de costos más estrictos")
    
    if desviacion > 0.05:
        recomendaciones.append("Analizar causas de desviación presupuestal")
        recomendaciones.append("Establecer alertas tempranas de sobrecostos")
    
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
    satisfaccion_score = proyectos_a_tiempo * 70 + (1 - proyectos_cancelados) * 30
    
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
    
    if proyectos_cancelados > 0.05:
        recomendaciones.append("Fortalecer análisis de viabilidad pre-proyecto")
        recomendaciones.append("Mejorar comunicación con stakeholders")
        recomendaciones.append("Establecer checkpoints de go/no-go tempranos")
    
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
    
    # Score de eficiencia (0-100, mayor es mejor)
    eficiencia_score = (
        (1 - tareas_retrasadas) * 33.33 +
        (1 - hitos_retrasados) * 33.33 +
        (1 - tasa_errores) * 33.33
    ) * 100
    
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
    # Normalizar productividad (asumiendo 0.75 como óptimo)
    productividad_norm = min(productividad / 0.75, 1.0) if productividad > 0 else 0
    precision_estimacion = 1 - abs(horas_relacion - 1.0)
    
    capacidad_score = (
        productividad_norm * 40 +
        tasa_exito_pruebas * 40 +
        precision_estimacion * 20
    ) * 100
    
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
    
    if productividad < 0.65:
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
