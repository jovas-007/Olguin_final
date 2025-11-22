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
    "cumplimiento_presupuesto": 0.9,
    "desviacion_presupuestal": 0.05,
    "penalizaciones_sobre_presupuesto": 0.02,
    "proyectos_a_tiempo": 0.85,
    "proyectos_cancelados": 0.05,
    "porcentaje_tareas_retrasadas": 0.1,
    "porcentaje_hitos_retrasados": 0.1,
    "tasa_errores": 0.05,
    "productividad_promedio": 0.75,
    "tasa_exito_pruebas": 0.9,
    "horas_relacion": 1.1,
}
