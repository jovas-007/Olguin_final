import numpy as np
import pandas as pd
from scipy.stats import rayleigh
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import streamlit as st


def preparar_features_target(df: pd.DataFrame):
    features = df[
        [
            "Presupuesto",
            "NumTrabajadores",
            "RetrasoInicioDias",
            "RetrasoFinalDias",
            "ProductividadPromedio",
        ]
    ]
    target = df["TotalErrores"]
    return features, target


@st.cache_data(show_spinner=False)
def entrenar_modelo(df_proyectos: pd.DataFrame) -> LinearRegression:
    features, target = preparar_features_target(df_proyectos)
    modelo = LinearRegression()
    modelo.fit(features, target)
    return modelo


def obtener_metricas_modelo(df_proyectos: pd.DataFrame, modelo: LinearRegression) -> dict:
    """Calcula métricas de desempeño del modelo"""
    features, target = preparar_features_target(df_proyectos)
    predicciones = modelo.predict(features)
    
    r2 = r2_score(target, predicciones)
    rmse = np.sqrt(mean_squared_error(target, predicciones))
    mae = np.mean(np.abs(target - predicciones))
    
    return {
        "r2": r2,
        "rmse": rmse,
        "mae": mae,
        "confianza": "Alta" if r2 > 0.7 else "Media" if r2 > 0.5 else "Baja"
    }


def rayleigh_curve(total_defectos: float, duracion: int, sigma: float) -> pd.DataFrame:
    tiempo = np.linspace(0, duracion, num=duracion + 1)
    cdf = rayleigh.cdf(tiempo, scale=sigma)
    defectos_acumulados = total_defectos * cdf
    return pd.DataFrame({"Tiempo": tiempo, "DefectosAcumulados": defectos_acumulados})


def calcular_sigma(duracion: int, complejidad: str) -> float:
    base = max(duracion / 4, 1)
    factor = {"baja": 0.8, "media": 1.0, "alta": 1.3}.get(complejidad, 1.0)
    return base * factor


def clasificar_nivel_riesgo(defectos: float, trabajadores: int, duracion: int) -> dict:
    """
    Clasifica el nivel de riesgo del proyecto basado en defectos predichos
    """
    # Calcular tasa de defectos por persona por semana
    tasa_defectos = defectos / (trabajadores * (duracion / 7))
    
    if tasa_defectos < 0.5:
        nivel = "Bajo"
        color = "#2e7d32"  # Verde
        icono = "[BAJO]"
    elif tasa_defectos < 1.5:
        nivel = "Medio"
        color = "#f9a825"  # Amarillo
        icono = "[MEDIO]"
    else:
        nivel = "Alto"
        color = "#c62828"  # Rojo
        icono = "[ALTO]"
    
    return {
        "nivel": nivel,
        "color": color,
        "icono": icono,
        "tasa": tasa_defectos
    }


def generar_recomendaciones(
    defectos: float,
    trabajadores: int,
    duracion: int,
    presupuesto: float,
    retraso_inicio: int,
    retraso_final: int,
    complejidad: str,
    riesgo: dict
) -> list:
    """
    Genera recomendaciones accionables basadas en la predicción
    """
    recomendaciones = []
    
    # 1. Recomendaciones por nivel de riesgo
    if riesgo["nivel"] == "Alto":
        recomendaciones.append({
            "tipo": "[CRÍTICO]",
            "titulo": "Nivel de Defectos Alto - Acción Inmediata Requerida",
            "acciones": [
                f"Incrementar equipo de QA en al menos {int(defectos / 30)} personas",
                "Implementar revisiones de código obligatorias (Code Review)",
                "Establecer daily meetings de seguimiento de calidad",
                "Considerar reducir alcance o extender duración del proyecto"
            ],
            "color": "#c62828"
        })
    elif riesgo["nivel"] == "Medio":
        recomendaciones.append({
            "tipo": "[IMPORTANTE]",
            "titulo": "Nivel de Defectos Moderado - Monitoreo Cercano",
            "acciones": [
                "Asignar dedicación parcial de QA desde el inicio",
                "Implementar testing automatizado básico",
                "Revisiones de código en módulos críticos",
                "Checkpoint de calidad en hito del 50%"
            ],
            "color": "#f9a825"
        })
    else:
        recomendaciones.append({
            "tipo": "[FAVORABLE]",
            "titulo": "Nivel de Defectos Bajo - Mantener Buenas Prácticas",
            "acciones": [
                "Continuar con estándares actuales de calidad",
                "Testing básico durante desarrollo",
                "Revisiones de código selectivas",
                "Monitoreo quincenal de métricas"
            ],
            "color": "#2e7d32"
        })
    
    # 2. Recomendaciones por duración
    if duracion < 12:  # Menos de 3 meses
        recomendaciones.append({
            "tipo": "[DURACIÓN]",
            "titulo": "Proyecto Corto - Sprint Intensivo",
            "acciones": [
                "Concentrar testing en semanas 2-3",
                "Preparar equipo completo desde día 1",
                "Evitar cambios de alcance durante ejecución",
                "Daily standups obligatorios"
            ],
            "color": "#1976d2"
        })
    elif duracion > 36:  # Más de 9 meses
        recomendaciones.append({
            "tipo": "[DURACIÓN]",
            "titulo": "Proyecto Largo - Gestión por Fases",
            "acciones": [
                "Dividir en al menos 3 fases con entregables",
                "Testing incremental cada 8-12 semanas",
                "Revisión de arquitectura en hito del 30%",
                "Considerar rotación de personal para prevenir burnout"
            ],
            "color": "#1976d2"
        })
    
    # 3. Recomendaciones por retrasos esperados
    if retraso_inicio > 3 or retraso_final > 5:
        recomendaciones.append({
            "tipo": "[RETRASOS]",
            "titulo": "Riesgo de Retrasos Significativos",
            "acciones": [
                f"Agregar {int((retraso_inicio + retraso_final) * 0.2)} días de buffer adicional",
                "Identificar dependencias críticas desde el inicio",
                "Establecer plan de contingencia para recursos",
                "Comunicación semanal de status a stakeholders"
            ],
            "color": "#d32f2f"
        })
    
    # 4. Recomendaciones por complejidad
    if complejidad == "alta":
        recomendaciones.append({
            "tipo": "[COMPLEJIDAD]",
            "titulo": "Complejidad Alta - Controles Adicionales",
            "acciones": [
                "Asignar desarrolladores Senior en módulos core",
                "Documentación técnica obligatoria",
                "Pair programming en funcionalidades complejas",
                "Sesiones de knowledge sharing semanales"
            ],
            "color": "#7b1fa2"
        })
    
    # 5. Recomendaciones por tamaño de equipo
    if trabajadores < 5:
        recomendaciones.append({
            "tipo": "[EQUIPO]",
            "titulo": "Equipo Pequeño - Optimizar Comunicación",
            "acciones": [
                "Maximizar comunicación directa (menos ceremonias)",
                "Cada miembro debe conocer el proyecto completo",
                "Evitar silos de conocimiento",
                "Backup cruzado entre roles"
            ],
            "color": "#00796b"
        })
    elif trabajadores > 10:
        recomendaciones.append({
            "tipo": "[EQUIPO]",
            "titulo": "Equipo Grande - Gestión de Coordinación",
            "acciones": [
                "Dividir en squads de 4-6 personas",
                "Designar tech leads por área",
                "Implementar integración continua obligatoria",
                "Sincronización inter-squad 2 veces por semana"
            ],
            "color": "#00796b"
        })
    
    return recomendaciones


def generar_plan_testing(defectos: float, duracion: int, curva: pd.DataFrame) -> pd.DataFrame:
    """
    Genera un plan de testing sugerido basado en la curva de Rayleigh
    """
    semanas = int(duracion / 7)
    plan = []
    
    for semana in range(1, semanas + 1):
        tiempo_semana = semana * 7
        idx = min(int(tiempo_semana), len(curva) - 1)
        
        defectos_acumulados = curva.iloc[idx]["DefectosAcumulados"]
        defectos_semana = defectos_acumulados - (curva.iloc[max(0, idx - 7)]["DefectosAcumulados"] if idx > 7 else 0)
        
        # Calcular esfuerzo de QA sugerido (proporción a defectos esperados)
        if defectos_semana > defectos * 0.15:  # Más del 15% en una semana
            esfuerzo = "Alto"
            recursos_qa = "2-3 QA"
        elif defectos_semana > defectos * 0.08:
            esfuerzo = "Medio"
            recursos_qa = "1-2 QA"
        else:
            esfuerzo = "Bajo"
            recursos_qa = "1 QA"
        
        plan.append({
            "Semana": semana,
            "Defectos Esperados": f"{defectos_semana:.1f}",
            "Esfuerzo QA": esfuerzo,
            "Recursos Sugeridos": recursos_qa
        })
    
    return pd.DataFrame(plan)


def buscar_proyectos_similares(
    df_proyectos: pd.DataFrame,
    presupuesto: float,
    trabajadores: int,
    complejidad: str
) -> pd.DataFrame:
    """
    Busca proyectos históricos con características similares
    """
    # Filtrar por rango de presupuesto (+/- 30%)
    presupuesto_min = presupuesto * 0.7
    presupuesto_max = presupuesto * 1.3
    
    similares = df_proyectos[
        (df_proyectos["Presupuesto"] >= presupuesto_min) &
        (df_proyectos["Presupuesto"] <= presupuesto_max) &
        (df_proyectos["NumTrabajadores"] >= trabajadores - 2) &
        (df_proyectos["NumTrabajadores"] <= trabajadores + 2)
    ].copy()
    
    if len(similares) > 0:
        similares = similares[[
            "CodigoProyecto",
            "Presupuesto",
            "CosteReal",
            "NumTrabajadores",
            "TotalErrores",
            "RetrasoFinalDias",
            "ProductividadPromedio"
        ]].head(5)
        
        similares["Desviacion%"] = ((similares["CosteReal"] - similares["Presupuesto"]) / similares["Presupuesto"] * 100).round(2)
    
    return similares
