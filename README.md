# DSS – Dashboard de desempeño de proyectos de software

## 🎯 Misión y Visión

**Misión:** Optimizar procesos con tecnología  
**Visión:** Decisiones basadas en datos y excelencia sostenible

---

## 📋 Descripción

Aplicación de Streamlit que implementa un **Balanced Scorecard**, análisis **OLAP multidimensional**, **predicción de defectos con IA** y **OKRs estratégicos** para el data warehouse `dw_proyectos`.

### Características principales

- ✅ **Balanced Scorecard:** 4 perspectivas estratégicas con predicciones de IA y 16+ recomendaciones accionables
- ✅ **Análisis OLAP:** 10+ vistas multidimensionales con drill-down, roll-up, slicing, dicing y pivot
- ✅ **Predicción de defectos:** Modelo de Machine Learning basado en distribución de Rayleigh
- ✅ **Métricas calculadas:** 12 indicadores técnicos calculados dinámicamente desde el DWH
- ✅ **OKRs:** 4 objetivos estratégicos con 12 Key Results medibles y seguimiento automático de progreso

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

## Credenciales de ejemplo
En `app.py` se definen usuarios de muestra:
- `pm1` / `1234` (rol `project_manager`, acceso a la predicción Rayleigh)
- `analista1` / `abcd` (rol `viewer`)

La aplicación muestra datos reales desde `dw_proyectos`; si la conexión falla, se cargan datos de ejemplo para mantener el dashboard funcional.
