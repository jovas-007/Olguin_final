# DSS – Dashboard de desempeño de proyectos de software

Aplicación de Streamlit que implementa un Balanced Scorecard, análisis OLAP y un módulo de predicción de defectos basado en distribución de Rayleigh para el data warehouse `dw_proyectos`.

## Requisitos
- Python 3
- Dependencias principales: `streamlit`, `pandas`, `numpy`, `sqlalchemy`, `mysql-connector-python`, `scikit-learn`, `scipy`.

## Configuración
1. Define las variables de entorno o ajusta el diccionario `DB_CONFIG` en `app.py`:
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

## Credenciales de ejemplo
En `app.py` se definen usuarios de muestra:
- `pm1` / `1234` (rol `project_manager`, acceso a la predicción Rayleigh)
- `analista1` / `abcd` (rol `viewer`)

La aplicación muestra datos reales desde `dw_proyectos`; si la conexión falla, se cargan datos de ejemplo para mantener el dashboard funcional.
