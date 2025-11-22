# DSS – Dashboard de desempeño de proyectos de software

Aplicación de Streamlit que implementa un Balanced Scorecard, análisis OLAP y un módulo de predicción de defectos basado en distribución de Rayleigh para el data warehouse `dw_proyectos`.

## Estructura
- `app.py`: punto de entrada de Streamlit que orquesta vistas y filtros.
- `dss/config.py`: configuración de conexión y metas de KPI.
- `dss/db.py`: creación de engine y conexión MySQL.
- `dss/data_sources.py`: carga de datos desde el DWH y generación de datos de respaldo.
- `dss/analytics.py`: cálculos de KPIs, filtros y vistas tipo cubo.
- `dss/prediction.py`: modelo de regresión y curva de Rayleigh.
- `dss/ui/`: componentes y vistas del dashboard.

## Requisitos
- Python 3
- Dependencias principales: `streamlit`, `pandas`, `numpy`, `sqlalchemy`, `mysql-connector-python`, `scikit-learn`, `scipy`.

## Configuración
1. Define las variables de entorno o ajusta el diccionario `DB_CONFIG` en `dss/config.py`:
   - `DB_HOST` (por defecto `localhost`)
   - `DB_PORT` (por defecto `3307`)
   - `DB_USER` (por defecto `root`)
   - `DB_PASSWORD`
   - `DB_NAME` (por defecto `dw_proyectos`)
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
   o manualmente:
   ```bash
   pip install streamlit pandas numpy sqlalchemy mysql-connector-python scikit-learn scipy
   ```

## Ejecución
Desde la raíz del proyecto:
```bash
streamlit run app.py
```

> Nota: ejecutar `python app.py` no carga el runtime completo de Streamlit y mostrará advertencias de `ScriptRunContext`. Usa siempre `streamlit run` para que la sesión, los formularios y el caché funcionen correctamente.

## Credenciales de ejemplo
En `app.py` se definen usuarios de muestra:
- `pm1` / `1234` (rol `project_manager`, acceso a la predicción Rayleigh)
- `analista1` / `abcd` (rol `viewer`)

La aplicación muestra datos reales desde `dw_proyectos`; si la conexión falla, se cargan datos de ejemplo para mantener el dashboard funcional.
