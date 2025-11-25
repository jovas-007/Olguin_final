"""
Definición de OKRs (Objectives and Key Results) del sistema
"""

OKRS = {
    "O1_Excelencia_Financiera": {
        "objetivo": "Maximizar rentabilidad y control de costos",
        "descripcion": "Asegurar que todos los proyectos se ejecuten dentro del presupuesto con mínimas desviaciones y penalizaciones",
        "key_results": [
            {
                "kr": "KR1.1",
                "descripcion": "Mantener desviación presupuestal ≤ 5%",
                "metrica": "desviacion_presupuestal",
                "target": 0.05,
                "unidad": "%",
                "peso": 40
            },
            {
                "kr": "KR1.2",
                "descripcion": "Reducir penalizaciones a ≤ 2% del presupuesto",
                "metrica": "penalizaciones_sobre_presupuesto",
                "target": 0.02,
                "unidad": "%",
                "peso": 30
            },
            {
                "kr": "KR1.3",
                "descripcion": "Lograr cumplimiento presupuestal ≥ 95%",
                "metrica": "cumplimiento_presupuesto",
                "target": 0.95,
                "unidad": "%",
                "peso": 30
            }
        ]
    },
    
    "O2_Satisfaccion_Cliente": {
        "objetivo": "Cumplir compromisos y superar expectativas",
        "descripcion": "Entregar proyectos a tiempo y con alta calidad para fidelizar clientes",
        "key_results": [
            {
                "kr": "KR2.1",
                "descripcion": "Entregar ≥ 85% de proyectos a tiempo",
                "metrica": "proyectos_a_tiempo",
                "target": 0.85,
                "unidad": "%",
                "peso": 50
            },
            {
                "kr": "KR2.2",
                "descripcion": "Mantener tasa de cancelación ≤ 5%",
                "metrica": "proyectos_cancelados",
                "target": 0.05,
                "unidad": "%",
                "peso": 30
            },
            {
                "kr": "KR2.3",
                "descripcion": "Reducir retrasos finales a 0 días promedio",
                "metrica": "retraso_final_dias",
                "target": 0,
                "unidad": "días",
                "peso": 20
            }
        ]
    },
    
    "O3_Procesos_Eficientes": {
        "objetivo": "Optimizar operaciones internas y calidad",
        "descripcion": "Reducir retrasos y errores mediante procesos eficientes y control de calidad",
        "key_results": [
            {
                "kr": "KR3.1",
                "descripcion": "Reducir tareas retrasadas a ≤ 10%",
                "metrica": "porcentaje_tareas_retrasadas",
                "target": 0.10,
                "unidad": "%",
                "peso": 30
            },
            {
                "kr": "KR3.2",
                "descripcion": "Mantener hitos retrasados ≤ 10%",
                "metrica": "porcentaje_hitos_retrasados",
                "target": 0.10,
                "unidad": "%",
                "peso": 30
            },
            {
                "kr": "KR3.3",
                "descripcion": "Reducir tasa de errores a ≤ 5%",
                "metrica": "tasa_errores",
                "target": 0.05,
                "unidad": "%",
                "peso": 40
            }
        ]
    },
    
    "O4_Equipos_Alto_Desempeño": {
        "objetivo": "Desarrollar talento y capacidades",
        "descripcion": "Maximizar productividad y calidad del trabajo mediante desarrollo continuo",
        "key_results": [
            {
                "kr": "KR4.1",
                "descripcion": "Lograr productividad promedio ≥ 40 horas/hito",
                "metrica": "productividad_promedio",
                "target": 40,
                "unidad": "hrs/hito",
                "peso": 35
            },
            {
                "kr": "KR4.2",
                "descripcion": "Alcanzar ≥ 90% de éxito en pruebas",
                "metrica": "tasa_exito_pruebas",
                "target": 0.90,
                "unidad": "%",
                "peso": 35
            },
            {
                "kr": "KR4.3",
                "descripcion": "Precisión de estimación dentro del ±10%",
                "metrica": "horas_relacion",
                "target": 1.10,
                "unidad": "ratio",
                "peso": 30
            }
        ]
    }
}


def calcular_progreso_okr(okr_key: str, kpis: dict) -> dict:
    """
    Calcula el progreso de un OKR basado en sus Key Results
    """
    okr = OKRS[okr_key]
    key_results_progreso = []
    peso_total = 0
    progreso_ponderado = 0
    
    for kr in okr["key_results"]:
        metrica_valor = kpis.get(kr["metrica"], 0)
        target = kr["target"]
        peso = kr["peso"]
        
        # Calcular progreso (0-100%)
        if kr["metrica"] in ["proyectos_cancelados", "desviacion_presupuestal", 
                             "penalizaciones_sobre_presupuesto", "porcentaje_tareas_retrasadas",
                             "porcentaje_hitos_retrasados", "tasa_errores", "retraso_final_dias"]:
            # Métricas donde menor es mejor
            if metrica_valor <= target:
                progreso = 100
            else:
                progreso = max(0, 100 - ((metrica_valor - target) / target * 100))
        else:
            # Métricas donde mayor es mejor
            if metrica_valor >= target:
                progreso = 100
            else:
                progreso = (metrica_valor / target) * 100 if target > 0 else 0
        
        key_results_progreso.append({
            "kr": kr["kr"],
            "descripcion": kr["descripcion"],
            "metrica_valor": metrica_valor,
            "target": target,
            "progreso": min(100, progreso),
            "peso": peso
        })
        
        peso_total += peso
        progreso_ponderado += progreso * peso
    
    progreso_general = progreso_ponderado / peso_total if peso_total > 0 else 0
    
    return {
        "objetivo": okr["objetivo"],
        "descripcion": okr["descripcion"],
        "progreso_general": progreso_general,
        "key_results": key_results_progreso
    }


def calcular_todos_okrs(kpis: dict) -> dict:
    """
    Calcula el progreso de todos los OKRs
    """
    return {
        okr_key: calcular_progreso_okr(okr_key, kpis)
        for okr_key in OKRS.keys()
    }
