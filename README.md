# DSS – Dashboard de desempeño de proyectos de software

## 🎯 Misión y Visión

**Misión:** Optimizar procesos con tecnología  
**Visión:** Decisiones basadas en datos y excelencia sostenible

---

## 📋 Descripción

Aplicación de Streamlit que implementa un **Balanced Scorecard**, análisis **OLAP multidimensional**, **predicción de defectos con IA** y **OKRs estratégicos** conectada a **TiDB Cloud** (base de datos MySQL compatible en la nube).

### Características principales

- ✅ **Balanced Scorecard:** 4 perspectivas estratégicas con predicciones de IA y 16+ recomendaciones accionables
- ✅ **Análisis OLAP:** 10+ vistas multidimensionales con drill-down, roll-up, slicing, dicing y pivot
- ✅ **Predicción de defectos:** Modelo de Machine Learning basado en distribución de Rayleigh
- ✅ **Métricas calculadas:** 12 indicadores técnicos calculados dinámicamente desde el DWH
- ✅ **OKRs:** 4 objetivos estratégicos con 12 Key Results medibles y seguimiento automático de progreso
- ✅ **Base de datos en la nube:** TiDB Cloud (AWS us-east-1) para escalabilidad y alta disponibilidad

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────┐
│           INTERFAZ WEB (Streamlit)              │
├─────────────────────────────────────────────────┤
│  📊 Balanced Scorecard  │  📈 Dashboard         │
│  ├─ BSC                 │  ├─ Análisis Visual   │
│  ├─ OKRs                │  ├─ Análisis Detallado│
│  └─ Predicción ML       │  └─ Métricas Calculadas│
├─────────────────────────────────────────────────┤
│           CAPA DE LÓGICA DE NEGOCIO             │
│  • analytics.py    • metricas_calculadas.py     │
│  • prediction.py   • okrs.py                    │
│  • db_config.py (NEW)                           │
├─────────────────────────────────────────────────┤
│        TIDB CLOUD - AWS (us-east-1)             │
│  • hechos_proyectos    • dim_proyectos          │
│  • hechos_asignaciones • dim_clientes           │
│  • dim_tiempo          • dim_empleados          │
│  • dim_gastos          • dim_hitos              │
│  • dim_tareas          • dim_pruebas            │
└─────────────────────────────────────────────────┘
```

## 📁 Estructura del Proyecto

- `app.py`: Punto de entrada de Streamlit que orquesta vistas y filtros
- `dss/config.py`: Configuración de metas de KPI y constantes
- `dss/db_config.py`: **[NUEVO]** Gestión de conexión a TiDB Cloud
- `dss/data_sources.py`: Carga de datos desde TiDB Cloud mediante queries SQL
- `dss/analytics.py`: Cálculos de KPIs, filtros y vistas tipo cubo
- `dss/prediction.py`: Modelo de regresión y curva de Rayleigh
- `dss/metricas_calculadas.py`: Cálculo de 12 métricas técnicas
- `dss/ui/`: Componentes y vistas del dashboard

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd Olguin_final
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Dependencias principales:**
- `streamlit` - Framework web
- `pandas` - Manipulación de datos
- `numpy` - Operaciones numéricas
- `pymysql` - Conector MySQL
- `python-dotenv` - Gestión de variables de entorno
- `cryptography` - Seguridad para conexiones SSL
- `scikit-learn` - Machine Learning
- `scipy` - Distribuciones estadísticas

### 3. Configurar credenciales de base de datos

Crear archivo `.env` en la raíz del proyecto:

```env
DW_HOST=gateway01.us-east-1.prod.aws.tidbcloud.com
DW_PORT=4000
DW_USER=<tu-usuario>
DW_PASS=<tu-password>
DW_DB=dw_proyectos
DW_SSL=true
```

**⚠️ IMPORTANTE:** 
- El archivo `.env` está en `.gitignore` para proteger credenciales
- **NUNCA** subir credenciales a repositorios públicos

### 4. Probar conexión

```bash
python test_db_connection.py
```

Deberías ver:
```
✅ Conexión exitosa a TiDB Cloud
✅ 4 proyectos cargados
✅ 1964 asignaciones cargadas
✅ PRUEBA COMPLETADA EXITOSAMENTE
```

### 5. Ejecutar la aplicación

```bash
streamlit run app.py
```

O:

```bash
python -m streamlit run app.py
```

La aplicación estará disponible en:
- **Local:** http://localhost:8501
- **Red:** http://<tu-ip>:8501

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
