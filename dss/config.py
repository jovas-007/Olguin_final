import os

# URL de conexión directa (formato que funciona)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root@localhost:3307/dw_proyectos?charset=utf8mb4"
)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3307)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "dw_proyectos"),
}

KPI_TARGETS = {
    # Métricas de Tiempo
    "retraso_inicio_dias": 0,  # Target: 0 días de retraso en inicio
    "retraso_final_dias": 0,  # Target: 0 días de retraso al finalizar
    
    # Métricas Financieras
    "cumplimiento_presupuesto": 0.95,  # 95% de cumplimiento
    "desviacion_presupuestal": 0.05,  # Máximo 5% de desviación
    "penalizaciones_sobre_presupuesto": 0.02,  # Máximo 2%
    
    # Métricas de Distribución Financiera
    "proporcion_capex_opex": 0.6,  # 60% CAPEX, 40% OPEX
    
    # Métricas de Calidad
    "tasa_errores": 0.05,  # Máximo 5% de tasa de errores
    "tasa_exito_pruebas": 0.9,  # Mínimo 90% de éxito en pruebas
    
    # Métricas de Productividad
    "productividad_promedio": 400,  # 400 horas por hito (baseline)
    
    # Métricas de Retrasos
    "porcentaje_tareas_retrasadas": 0.1,  # Máximo 10%
    "porcentaje_hitos_retrasados": 0.1,  # Máximo 10%
    
    # Métricas Complementarias (mantenidas para compatibilidad)
    "proyectos_a_tiempo": 0.85,  # 85% de proyectos a tiempo
    "proyectos_cancelados": 0.05,  # Máximo 5% cancelados
    "horas_relacion": 1.1,  # Relación horas reales/planificadas <= 110%
}
