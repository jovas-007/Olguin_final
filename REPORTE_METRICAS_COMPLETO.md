# REPORTE COMPLETO DE MÉTRICAS, KPIs, OKRs Y CUBO OLAP
## DSS – Dashboard de Desempeño de Proyectos de Software

---

## 📊 RESUMEN EJECUTIVO

Este sistema de soporte a decisiones (DSS) implementa un **Balanced Scorecard** con arquitectura **OLAP** para análisis multidimensional de proyectos de software. Incluye:

- **11 KPIs estratégicos** con targets definidos
- **8 métricas calculadas dinámicamente** desde el data warehouse
- **Cubo OLAP** con modelo estrella (2 tablas de hechos, 7 dimensiones)
- **5 perspectivas de análisis** (Financiera, Cliente, Procesos, Aprendizaje, Predicción)
- **Sistema de predicción** basado en distribución de Rayleigh

---

## 🎯 1. KPIs ESTRATÉGICOS (Key Performance Indicators)

### 1.1 Perspectiva Financiera

#### KPI 1: Cumplimiento de Presupuesto
- **Definición**: Proporción del presupuesto ejecutado correctamente
- **Fórmula**: `1 - ((CosteReal - Presupuesto) / Presupuesto)`
- **Target**: **≥ 90%** (0.9)
- **Fuente**: `hechos_proyectos.Presupuesto`, `hechos_proyectos.CosteReal`
- **Perspectiva BSC**: Financiera
- **OKR Relacionado**: Optimizar eficiencia financiera al 90%
- **Interpretación**: 
  - ✅ > 90%: Excelente control financiero
  - ⚠️ 80-90%: Control aceptable, requiere monitoreo
  - ❌ < 80%: Riesgo financiero crítico

#### KPI 2: Desviación Presupuestal Promedio
- **Definición**: Diferencia promedio entre costo real y presupuesto planificado
- **Fórmula**: `MEAN(DesviacionPresupuestal)`
- **Target**: **≤ 5%** (0.05)
- **Fuente**: `hechos_proyectos.DesviacionPresupuestal`
- **Perspectiva BSC**: Financiera
- **OKR Relacionado**: Reducir desviaciones presupuestales bajo 5%
- **Interpretación**:
  - ✅ < 5%: Control de costos óptimo
  - ⚠️ 5-10%: Requiere análisis de causas
  - ❌ > 10%: Planificación financiera deficiente

#### KPI 3: Penalizaciones sobre Presupuesto
- **Definición**: Proporción del presupuesto perdido en penalizaciones contractuales
- **Fórmula**: `MEAN(PenalizacionesMonto / Presupuesto)`
- **Target**: **≤ 2%** (0.02)
- **Fuente**: `hechos_proyectos.PenalizacionesMonto`, `hechos_proyectos.Presupuesto`
- **Perspectiva BSC**: Financiera
- **OKR Relacionado**: Minimizar riesgo contractual a menos del 2%
- **Interpretación**:
  - ✅ < 2%: Cumplimiento contractual excelente
  - ⚠️ 2-5%: Revisar SLAs y compromisos
  - ❌ > 5%: Riesgo de pérdida de clientes

---

### 1.2 Perspectiva del Cliente

#### KPI 4: Proyectos Entregados a Tiempo
- **Definición**: Proporción de proyectos finalizados sin retraso
- **Fórmula**: `COUNT(RetrasoFinalDias <= 0) / COUNT(Proyectos)`
- **Target**: **≥ 85%** (0.85)
- **Fuente**: `hechos_proyectos.RetrasoFinalDias`
- **Perspectiva BSC**: Cliente
- **OKR Relacionado**: Alcanzar 85% de entregas puntuales
- **Interpretación**:
  - ✅ > 85%: Alta confiabilidad
  - ⚠️ 70-85%: Requiere mejora en planificación
  - ❌ < 70%: Pérdida de confianza del cliente

#### KPI 5: Proyectos Cancelados
- **Definición**: Proporción de proyectos cancelados antes de finalizar
- **Fórmula**: `COUNT(Cancelado = 1) / COUNT(Proyectos)`
- **Target**: **≤ 5%** (0.05)
- **Fuente**: `dim_proyectos.Cancelado`
- **Perspectiva BSC**: Cliente
- **OKR Relacionado**: Mantener tasa de cancelación bajo 5%
- **Interpretación**:
  - ✅ < 5%: Gestión de riesgos efectiva
  - ⚠️ 5-10%: Revisar proceso de viabilidad
  - ❌ > 10%: Problemas en selección de proyectos

---

### 1.3 Perspectiva de Procesos Internos

#### KPI 6: Porcentaje de Tareas Retrasadas
- **Definición**: Proporción de tareas individuales no completadas a tiempo
- **Fórmula**: `MEAN(PorcentajeTareasRetrasadas)`
- **Target**: **≤ 10%** (0.1)
- **Fuente**: `hechos_proyectos.PorcentajeTareasRetrasadas`
- **Perspectiva BSC**: Procesos Internos
- **OKR Relacionado**: Reducir tareas retrasadas a menos del 10%
- **Cálculo detallado**: Ver Métrica Calculada #4
- **Interpretación**:
  - ✅ < 10%: Operación ágil
  - ⚠️ 10-20%: Revisar carga de trabajo
  - ❌ > 20%: Problemas de capacidad

#### KPI 7: Porcentaje de Hitos Retrasados
- **Definición**: Proporción de hitos no alcanzados en fecha planificada
- **Fórmula**: `MEAN(PorcentajeHitosRetrasados)`
- **Target**: **≤ 10%** (0.1)
- **Fuente**: `hechos_proyectos.PorcentajeHitosRetrasados`
- **Perspectiva BSC**: Procesos Internos
- **OKR Relacionado**: Lograr 90% de hitos a tiempo
- **Cálculo detallado**: Ver Métrica Calculada #5
- **Interpretación**:
  - ✅ < 10%: Disciplina de entrega alta
  - ⚠️ 10-20%: Necesita refuerzo de seguimiento
  - ❌ > 20%: Planificación deficiente

#### KPI 8: Tasa de Errores Encontrados
- **Definición**: Proporción de defectos encontrados respecto al volumen de código
- **Fórmula**: `MEAN(TasaDeErroresEncontrados)`
- **Target**: **≤ 5%** (0.05)
- **Fuente**: `hechos_proyectos.TasaDeErroresEncontrados`
- **Perspectiva BSC**: Procesos Internos
- **OKR Relacionado**: Mantener tasa de defectos bajo 5%
- **Interpretación**:
  - ✅ < 5%: Alta calidad de código
  - ⚠️ 5-10%: Reforzar code reviews
  - ❌ > 10%: Problemas críticos de calidad

---

### 1.4 Perspectiva de Aprendizaje e Innovación

#### KPI 9: Productividad Promedio
- **Definición**: Eficiencia general del equipo de desarrollo
- **Fórmula**: `MEAN(ProductividadPromedio)`
- **Target**: **≥ 75%** (0.75)
- **Fuente**: `hechos_proyectos.ProductividadPromedio`
- **Perspectiva BSC**: Aprendizaje e Innovación
- **OKR Relacionado**: Alcanzar 75% de productividad óptima
- **Cálculo detallado**: Ver Métrica Calculada #3
- **Interpretación**:
  - ✅ > 75%: Equipo altamente eficiente
  - ⚠️ 60-75%: Oportunidades de mejora
  - ❌ < 60%: Requiere capacitación o reorganización

#### KPI 10: Tasa de Éxito en Pruebas
- **Definición**: Proporción de pruebas exitosas del total ejecutado
- **Fórmula**: `MEAN(TasaDeExitoEnPruebas)`
- **Target**: **≥ 90%** (0.9)
- **Fuente**: `hechos_proyectos.TasaDeExitoEnPruebas`
- **Perspectiva BSC**: Aprendizaje e Innovación
- **OKR Relacionado**: Lograr 90% de éxito en testing
- **Interpretación**:
  - ✅ > 90%: Testing efectivo
  - ⚠️ 80-90%: Mejorar estrategia de pruebas
  - ❌ < 80%: QA insuficiente

#### KPI 11: Relación Horas Reales/Planificadas
- **Definición**: Proporción entre horas trabajadas y horas estimadas
- **Fórmula**: `SUM(HorasReales) / SUM(HorasPlanificadas)`
- **Target**: **≤ 110%** (1.1)
- **Fuente**: `hechos_asignaciones.HorasReales`, `hechos_asignaciones.HorasPlanificadas`
- **Perspectiva BSC**: Aprendizaje e Innovación
- **OKR Relacionado**: Precisión de estimación dentro del 10%
- **Interpretación**:
  - ✅ 0.9-1.1: Estimación precisa
  - ⚠️ 1.1-1.3: Subestimación moderada
  - ❌ > 1.3 o < 0.7: Problemas de planificación

---

## 📈 2. MÉTRICAS CALCULADAS DINÁMICAMENTE

### 2.1 Métrica: DuracionRealDias
- **Definición**: Número de días calendario entre inicio y finalización real del proyecto
- **Fórmula**: `FechaFinalizacionReal - FechaInicio`
- **Fuente de Datos**: 
  - `dim_tiempo` (tabla de dimensión temporal)
  - `hechos_proyectos.ID_FechaInicio`, `hechos_proyectos.ID_FechaFin`
- **Cálculo**: 
  ```python
  fecha_inicio_dt = pd.to_datetime(f"{Anio}-{Mes}-{Dia}")
  fecha_fin_dt = pd.to_datetime(f"{Anio}-{Mes}-{Dia}")
  duracion_dias = (fecha_fin_dt - fecha_inicio_dt).days
  ```
- **Función**: `calcular_duracion_real_dias()`
- **Archivo**: `dss/metricas_calculadas.py`
- **Uso**: Análisis de duración de proyectos, comparación con estimaciones

---

### 2.2 Métrica: NumeroDefectosEncontrados
- **Definición**: Total de defectos identificados durante pruebas (pruebas fallidas)
- **Fórmula**: `COUNT(ID_Prueba WHERE PruebaExitosa = 0)`
- **Fuente de Datos**:
  - `dim_pruebas` (dimensión de pruebas de calidad)
  - `dim_hitos` (para relacionar pruebas con proyectos)
- **Cálculo**:
  ```python
  hitos_proyecto = dim_hitos[dim_hitos["ID_proyectos"] == id_proyecto]
  pruebas_fallidas = dim_pruebas[
      (dim_pruebas["ID_Hito"].isin(hitos)) & 
      (dim_pruebas["PruebaExitosa"] == 0)
  ]
  defectos = len(pruebas_fallidas)
  ```
- **Función**: `calcular_numero_defectos_encontrados()`
- **Uso**: Predicción de defectos (modelo Rayleigh), análisis de calidad

---

### 2.3 Métrica: ProductividadPromedio
- **Definición**: Días de duración por empleado (menor es mejor)
- **Fórmula**: `DuracionReal / No_empleados`
- **Fuente de Datos**:
  - Métrica calculada: `DuracionRealDias`
  - `dim_proyectos.NumTrabajadores`
- **Cálculo**:
  ```python
  duracion_dias = calcular_duracion_real_dias(id_proyecto)
  num_empleados = dim_proyectos["NumTrabajadores"]
  productividad = duracion_dias / num_empleados if num_empleados > 0 else 0
  ```
- **Función**: `calcular_productividad_promedio()`
- **Uso**: KPI #9, comparación de eficiencia entre proyectos

---

### 2.4 Métrica: PorcentajeTareasRetrasadas
- **Definición**: Proporción de tareas del proyecto que no se completaron a tiempo
- **Fórmula**: `(COUNT(TareasRetrasadas) / COUNT(TareasTotales)) × 100`
- **Fuente de Datos**:
  - `dim_tareas` (dimensión de tareas del proyecto)
  - `dim_tareas.SeRetraso` (flag booleano 0/1)
- **Cálculo**:
  ```python
  hitos_proyecto = dim_hitos[dim_hitos["ID_proyectos"] == id_proyecto]
  tareas = dim_tareas[dim_tareas["ID_Hito"].isin(hitos)]
  tareas_retrasadas = (tareas["SeRetraso"] == 1).sum()
  porcentaje = (tareas_retrasadas / len(tareas)) * 100
  ```
- **Función**: `calcular_porcentaje_tareas_retrasadas()`
- **Uso**: KPI #6, análisis de procesos internos

---

### 2.5 Métrica: PorcentajeHitosRetrasados
- **Definición**: Proporción de hitos (milestones) con retraso en su finalización
- **Fórmula**: `(COUNT(HitosRetrasados) / COUNT(HitosTotales)) × 100`
- **Fuente de Datos**:
  - `dim_hitos`
  - `dim_hitos.RetrasoFinDias` (días de retraso, > 0 indica retraso)
- **Cálculo**:
  ```python
  hitos_proyecto = dim_hitos[dim_hitos["ID_proyectos"] == id_proyecto]
  hitos_retrasados = (hitos_proyecto["RetrasoFinDias"] > 0).sum()
  porcentaje = (hitos_retrasados / len(hitos_proyecto)) * 100
  ```
- **Función**: `calcular_porcentaje_hitos_retrasados()`
- **Uso**: KPI #7, detección de problemas en fases críticas

---

### 2.6 Métrica: CostoReal (Desglosado)
- **Definición**: Costo total del proyecto (mano de obra + gastos operativos)
- **Fórmula**: `Σ(CostoPorHoraEmpleado × HorasReales) + Σ GastosFinancieros`
- **Fuente de Datos**:
  - `hechos_asignaciones.ValorHoras` (costo por hora × horas)
  - `dim_gastos.Monto` (gastos financieros asociados)
- **Cálculo**:
  ```python
  asignaciones = hechos_asignaciones[hechos_asignaciones["ID_Proyecto"] == id]
  costo_horas = asignaciones["ValorHoras"].sum()
  
  id_gasto = hechos_proyectos["ID_Gasto"]
  gasto = dim_gastos[dim_gastos["ID_Finanza"] == id_gasto]
  gasto_financiero = gasto["Monto"].sum()
  
  costo_total = costo_horas + gasto_financiero
  ```
- **Función**: `calcular_costo_real_detallado()`
- **Retorna**: Diccionario con `{costo_horas, gasto_financiero, costo_total}`
- **Uso**: Análisis financiero detallado, comparación con presupuesto

---

### 2.7 Estadísticas Agregadas de Métricas Calculadas
Función: `obtener_estadisticas_metricas_calculadas()`

Retorna diccionario con:
- `duracion_promedio_dias`: Media de duración de proyectos
- `defectos_promedio`: Promedio de defectos por proyecto
- `defectos_total`: Suma total de defectos encontrados
- `productividad_calculada`: Media de productividad
- `tareas_retrasadas_calculada`: Media de % de tareas retrasadas
- `hitos_retrasados_calculada`: Media de % de hitos retrasados
- `costo_real_promedio`: Media del costo real calculado

**Uso**: Dashboard "Métricas Calculadas", análisis de tendencias

---

## 🧊 3. CUBO OLAP - ARQUITECTURA

### 3.1 Modelo de Datos: Esquema Estrella (Star Schema)

#### Tablas de Hechos (Fact Tables)

**Tabla: hechos_proyectos**
- **Propósito**: Métricas y medidas de desempeño de proyectos
- **Granularidad**: 1 fila por proyecto
- **Dimensiones relacionadas**: ID_Proyecto, ID_Cliente, ID_Gasto, ID_FechaInicio, ID_FechaFin
- **Medidas**:
  - `Presupuesto` (numérico)
  - `CosteReal` (numérico)
  - `DesviacionPresupuestal` (numérico)
  - `PenalizacionesMonto` (numérico)
  - `RetrasoInicioDias` (numérico)
  - `RetrasoFinalDias` (numérico)
  - `TasaDeErroresEncontrados` (decimal 0-1)
  - `TasaDeExitoEnPruebas` (decimal 0-1)
  - `ProductividadPromedio` (decimal)
  - `PorcentajeTareasRetrasadas` (decimal 0-1)
  - `PorcentajeHitosRetrasados` (decimal 0-1)
  - `ProporcionCAPEX_OPEX` (decimal 0-1)
- **Claves foráneas**: ID_Proyecto, ID_Cliente, ID_Gasto, ID_FechaInicio, ID_FechaFin

**Tabla: hechos_asignaciones**
- **Propósito**: Métricas de asignación de recursos humanos
- **Granularidad**: 1 fila por empleado-proyecto-período
- **Dimensiones relacionadas**: ID_Empleado, ID_Proyecto, ID_FechaAsignacion
- **Medidas**:
  - `HorasPlanificadas` (numérico)
  - `HorasReales` (numérico)
  - `ValorHoras` (numérico - costo)
  - `RetrasoHoras` (numérico)
- **Claves foráneas**: ID_Empleado, ID_Proyecto, ID_FechaAsignacion

---

#### Tablas de Dimensiones (Dimension Tables)

**Dimensión: dim_proyectos**
- **Atributos**: 
  - `ID_Proyecto` (PK)
  - `CodigoProyecto` (código de negocio)
  - `Version` (versión del proyecto)
  - `Cancelado` (flag 0/1)
  - `TotalErrores` (numérico)
  - `NumTrabajadores` (numérico)
- **Uso**: Clasificación y filtrado de proyectos

**Dimensión: dim_clientes**
- **Atributos**:
  - `ID_Cliente` (PK)
  - `CodigoClienteReal` (código de negocio)
  - Otros atributos de cliente
- **Uso**: Análisis por cliente, segmentación

**Dimensión: dim_empleados**
- **Atributos**:
  - `ID_Empleado` (PK)
  - `CodigoEmpleado` (código de negocio)
  - `Rol` (Developer, QA, PM, etc.)
  - `Seniority` (Junior, Semi, Senior)
- **Uso**: Análisis de recursos humanos, productividad por rol

**Dimensión: dim_tiempo**
- **Atributos**:
  - `ID_Tiempo` (PK)
  - `Anio` (año)
  - `Mes` (mes 1-12)
  - `Dia` (día del mes)
- **Uso**: Drill-down temporal, series de tiempo
- **Nota**: Reutilizada para FechaInicio, FechaFin, FechaAsignacion

**Dimensión: dim_gastos (dim_finanzas)**
- **Atributos**:
  - `ID_Finanza` (PK)
  - `TipoGasto` (Licencias, Viajes, Servicios, Capacitacion)
  - `Categoria` (CAPEX, OPEX)
  - `Monto` (numérico)
- **Uso**: Clasificación financiera, análisis CAPEX/OPEX

**Dimensión: dim_hitos**
- **Atributos**:
  - `ID_Hito` (PK)
  - `ID_proyectos` (FK a proyectos)
  - `RetrasoFinDias` (numérico)
- **Uso**: Cálculo de PorcentajeHitosRetrasados

**Dimensión: dim_tareas**
- **Atributos**:
  - `ID_Tarea` (PK)
  - `ID_Hito` (FK a hitos)
  - `SeRetraso` (flag 0/1)
- **Uso**: Cálculo de PorcentajeTareasRetrasadas

**Dimensión: dim_pruebas**
- **Atributos**:
  - `ID_Prueba` (PK)
  - `ID_Hito` (FK a hitos)
  - `PruebaExitosa` (flag 0/1)
- **Uso**: Cálculo de NumeroDefectosEncontrados

---

### 3.2 Operaciones OLAP Implementadas

#### SLICE (Corte)
**Implementación**: `aplicar_filtros()`, `aplicar_filtros_asignaciones()`
**Archivo**: `dss/analytics.py`

Filtrado por una dimensión:
```python
# Ejemplo: Slice por año
df_filtrado = df[df["AnioFin"].isin([2024])]

# Ejemplo: Slice por cliente
df_filtrado = df[df["CodigoClienteReal"].isin([501, 502])]

# Ejemplo: Slice por rol
df_filtrado = df[df["Rol"].isin(["Developer"])]
```

**Uso en Dashboard**: Multiselect en sidebar para cada dimensión

---

#### DICE (Dados múltiples)
**Implementación**: Combinación de filtros en `aplicar_filtros()`

Filtrado por múltiples dimensiones simultáneamente:
```python
filtros = {
    "anio": [2023, 2024],
    "mes": [1, 2, 3],
    "cliente": [501, 502],
    "proyecto": [1001, 1002]
}
# Aplica todos los filtros en cascada
```

**Uso en Dashboard**: Combinación de selecciones en sidebar

---

#### DRILL-DOWN (Descenso)
**Implementación**: Navegación jerárquica temporal y organizacional

**Jerarquía Temporal**:
```
Año → Mes → Día → Proyecto individual
```

**Jerarquía Organizacional**:
```
Todos los proyectos → Cliente → Proyecto → Tarea/Hito
```

**Ejemplo en código**:
```python
# Nivel 1: Todos los años
get_kpis(df_proyectos, df_asignaciones, {"anio": []})

# Nivel 2: Drill-down a 2024
get_kpis(df_proyectos, df_asignaciones, {"anio": [2024]})

# Nivel 3: Drill-down a enero 2024
get_kpis(df_proyectos, df_asignaciones, {"anio": [2024], "mes": [1]})

# Nivel 4: Drill-down a proyecto específico
get_detail_table(df_proyectos, {"proyecto": [1001]})
```

**Uso en Dashboard**: Tabs (Resumen → Análisis Detallado → Tabla)

---

#### ROLL-UP (Agregación)
**Implementación**: Funciones de agregación en `build_olap_views()`

**Agregaciones implementadas**:

1. **Por Categoría Financiera** (CAPEX/OPEX):
```python
capex_opex = proyectos.groupby("Categoria")["ProporcionCAPEX_OPEX"].mean()
```

2. **Por Rol de Empleado**:
```python
productividad_por_rol = asignaciones.groupby("Rol")[
    ["HorasReales", "HorasPlanificadas"]
].sum()
```

3. **Por Período Temporal**:
```python
proyectos_a_tiempo = proyectos.groupby(
    proyectos["FechaFin"].dt.to_period("M")
)["A_Tiempo"].mean()
```

4. **Métricas Globales** (KPIs):
```python
cumplimiento_presupuesto = (
    (1 - (proyectos["CosteReal"] - proyectos["Presupuesto"]) / 
     proyectos["Presupuesto"]).mean()
)
```

---

#### PIVOT (Rotación)
**Implementación**: Restructuración de datos para visualización

**Ejemplo - Presupuesto vs Real por Proyecto**:
```python
# Datos originales (orientación de filas)
CodigoProyecto | Presupuesto | CosteReal
1001           | 500000      | 520000
1002           | 300000      | 280000

# Pivot para gráfico (índice = proyecto, columnas = métricas)
barras_presupuesto = proyectos[["CodigoProyecto", "Presupuesto", "CosteReal"]]
chart_data = barras_presupuesto.set_index("CodigoProyecto")
```

**Uso en Dashboard**: `st.bar_chart()`, `st.line_chart()` con datos pivoteados

---

### 3.3 Vistas Materializadas del Cubo OLAP

Función: `build_olap_views()`
**Archivo**: `dss/analytics.py`

Retorna diccionario con 6 vistas pre-calculadas:

1. **barras_presupuesto**
   - Tipo: Comparación financiera
   - Columnas: `CodigoProyecto`, `Presupuesto`, `CosteReal`
   - Uso: Gráfico de barras en BSC

2. **proyectos_a_tiempo**
   - Tipo: Serie temporal
   - Columnas: `Fecha`, `A_Tiempo` (proporción 0-1)
   - Agregación: Por mes (`dt.to_period("M")`)
   - Uso: Gráfico de línea de entregas

3. **capex_opex**
   - Tipo: Distribución categórica
   - Columnas: `Categoria`, `ProporcionCAPEX_OPEX`
   - Agregación: Media por categoría
   - Uso: Gráfico de barras financiero

4. **retrasos**
   - Tipo: Comparación de retrasos
   - Columnas: `CodigoProyecto`, `RetrasoInicioDias`, `RetrasoFinalDias`
   - Uso: Análisis de gestión de cronograma

5. **productividad_por_rol**
   - Tipo: Agregación por dimensión empleado
   - Columnas: `Rol`, `HorasReales`, `HorasPlanificadas`
   - Agregación: Suma por rol
   - Uso: Análisis de eficiencia de recursos humanos

6. **asignaciones**
   - Tipo: Detalle granular
   - Columnas: Todas las de hechos_asignaciones
   - Uso: Tabla detallada de recursos

---

### 3.4 Arquitectura del Cubo

**Tipo de OLAP**: **ROLAP** (Relational OLAP)

**Características**:
- ✅ Datos almacenados en RDBMS (MySQL)
- ✅ Operaciones realizadas con SQL y Pandas
- ✅ No requiere cubo multidimensional físico (MOLAP)
- ✅ Cacheo en memoria para rendimiento (`@st.cache_data`)
- ✅ Escalable mediante índices en BD

**Flujo de Procesamiento**:
```
CSV/MySQL → Pandas DataFrame → Filtros OLAP → Agregaciones → Cache → Visualización
```

**Ventajas de esta implementación**:
- Simplicidad: No requiere servidor OLAP especializado
- Flexibilidad: Fácil agregar nuevas dimensiones/métricas
- Portabilidad: Funciona con CSV o MySQL
- Costo: Sin licencias de software OLAP comercial

---

## 🎯 4. OKRS (Objectives and Key Results)

### 4.1 Objetivo Estratégico 1: Excelencia Financiera
**Objetivo**: Maximizar rentabilidad y control de costos

**Key Results**:
1. KR1: Cumplimiento de presupuesto ≥ 90% en todos los proyectos activos
   - Métrica: KPI #1 (Cumplimiento de presupuesto)
   - Medición: Trimestral
   
2. KR2: Reducir desviación presupuestal promedio a ≤ 5%
   - Métrica: KPI #2 (Desviación presupuestal)
   - Medición: Mensual
   
3. KR3: Mantener penalizaciones contractuales bajo 2% del presupuesto total
   - Métrica: KPI #3 (Penalizaciones)
   - Medición: Por proyecto

---

### 4.2 Objetivo Estratégico 2: Satisfacción y Fidelización del Cliente
**Objetivo**: Cumplir compromisos y superar expectativas

**Key Results**:
1. KR1: Entregar ≥ 85% de proyectos a tiempo
   - Métrica: KPI #4 (Proyectos a tiempo)
   - Medición: Trimestral
   
2. KR2: Reducir tasa de cancelación de proyectos a ≤ 5%
   - Métrica: KPI #5 (Proyectos cancelados)
   - Medición: Anual
   
3. KR3: Lograr NPS (Net Promoter Score) > 50
   - Métrica: Externa (encuestas)
   - Medición: Semestral

---

### 4.3 Objetivo Estratégico 3: Procesos Eficientes y Calidad
**Objetivo**: Optimizar operaciones internas

**Key Results**:
1. KR1: Reducir tareas retrasadas a ≤ 10%
   - Métrica: KPI #6 (Tareas retrasadas) + Métrica Calculada #4
   - Medición: Sprint/Quincenal
   
2. KR2: Alcanzar ≤ 10% de hitos retrasados
   - Métrica: KPI #7 (Hitos retrasados) + Métrica Calculada #5
   - Medición: Mensual
   
3. KR3: Mantener tasa de errores ≤ 5%
   - Métrica: KPI #8 (Tasa de errores)
   - Medición: Por sprint

---

### 4.4 Objetivo Estratégico 4: Equipos de Alto Desempeño
**Objetivo**: Desarrollar talento y capacidades

**Key Results**:
1. KR1: Alcanzar productividad promedio ≥ 75%
   - Métrica: KPI #9 (Productividad) + Métrica Calculada #3
   - Medición: Mensual
   
2. KR2: Lograr ≥ 90% de éxito en pruebas
   - Métrica: KPI #10 (Tasa de éxito en pruebas)
   - Medición: Por sprint
   
3. KR3: Precisión de estimación dentro del ±10%
   - Métrica: KPI #11 (Relación horas)
   - Medición: Por proyecto

---

### 4.5 Objetivo Estratégico 5: Predicción y Gestión de Riesgos
**Objetivo**: Anticipar problemas antes de que ocurran

**Key Results**:
1. KR1: Predecir defectos con precisión ≥ 85%
   - Métrica: MAE, RMSE del modelo Rayleigh
   - Medición: Por proyecto (validación)
   
2. KR2: Identificar 100% de proyectos de alto riesgo antes de fase crítica
   - Métrica: Clasificación de riesgo (modelo predictivo)
   - Medición: Continua
   
3. KR3: Reducir tiempo de detección de problemas en 30%
   - Métrica: Dashboard de alertas tempranas
   - Medición: Trimestral

---

## 🔮 5. MÓDULO DE PREDICCIÓN (Modelo Rayleigh)

### 5.1 Propósito
Predecir la distribución temporal de defectos en proyectos de software

### 5.2 Fundamento Teórico
**Distribución de Rayleigh**: Modelo probabilístico usado en ingeniería de software para:
- Predecir cuándo se encontrarán la mayoría de los defectos
- Estimar el total de defectos al final del proyecto
- Planificar recursos de testing y QA

**Fórmula**:
```
f(t) = (t / σ²) * exp(-t² / 2σ²)
```
Donde:
- `t`: Tiempo transcurrido
- `σ`: Parámetro de escala (calculado desde datos históricos)

### 5.3 Implementación Técnica

**Función**: `entrenar_modelo()`
**Archivo**: `dss/prediction.py`

**Paso 1: Preparación de datos**
```python
X = df[["DuracionRealDias", "NumTrabajadores", "ProductividadPromedio"]]
y = df["TotalErrores"]
```

**Paso 2: Modelo de Regresión**
```python
from sklearn.ensemble import RandomForestRegressor
modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)
```

**Paso 3: Cálculo de σ (sigma)**
```python
def calcular_sigma(duracion_dias: float) -> float:
    return duracion_dias / np.sqrt(2)
```

**Paso 4: Generación de Curva Rayleigh**
```python
def rayleigh_curve(t: np.ndarray, sigma: float) -> np.ndarray:
    return (t / sigma**2) * np.exp(-t**2 / (2 * sigma**2))
```

### 5.4 Métricas del Modelo

**Función**: `obtener_metricas_modelo()`

**Métricas reportadas**:
1. **MAE** (Mean Absolute Error): Error promedio absoluto
2. **RMSE** (Root Mean Squared Error): Error cuadrático medio
3. **R²** (Coeficiente de determinación): Bondad de ajuste (0-1)

### 5.5 Clasificación de Riesgo

**Función**: `clasificar_nivel_riesgo()`

**Criterios**:
- **BAJO**: defectos_predichos < 100 Y productividad > 0.75
- **MEDIO**: 100 ≤ defectos_predichos ≤ 200 O productividad 0.65-0.75
- **ALTO**: defectos_predichos > 200 O productividad < 0.65

### 5.6 Sistema de Recomendaciones

**Función**: `generar_recomendaciones()`

**Recomendaciones por nivel de riesgo**:

**ALTO**:
- Reforzar equipo de QA (aumentar 30% de recursos de testing)
- Implementar code reviews obligatorias
- Realizar testing continuo desde fase temprana
- Considerar reducir alcance o extender cronograma

**MEDIO**:
- Monitoreo semanal de defectos encontrados
- Incrementar cobertura de pruebas automatizadas
- Revisiones de código para módulos críticos

**BAJO**:
- Mantener prácticas actuales
- Continuar con plan de testing estándar
- Monitoreo quincenal de KPIs

### 5.7 Plan de Testing Automático

**Función**: `generar_plan_testing()`

**Parámetros calculados**:
```python
plan = {
    "fase_pico_defectos": duracion_dias * 0.7,  # 70% del proyecto
    "recursos_qa_necesarios": ceil(defectos_predichos / 50),
    "horas_testing_recomendadas": defectos_predichos * 2,
    "cobertura_minima_codigo": 80% si ALTO, 70% si MEDIO, 60% si BAJO
}
```

### 5.8 Proyectos Similares

**Función**: `buscar_proyectos_similares()`

**Criterio de similitud**:
- Duración ± 20%
- Número de trabajadores ± 2
- Mismo rango de presupuesto (±30%)

**Uso**: Benchmarking y lecciones aprendidas

---

## 📊 6. VISTAS DEL DASHBOARD

### 6.1 Vista 1: Resumen General (Balanced Scorecard)
**Función**: `render_scorecard()`
**Archivo**: `dss/ui/views.py`

**Contenido**:
- **Perspectiva Financiera** (3 KPIs):
  - Cumplimiento de presupuesto
  - Desviación presupuestal
  - Penalizaciones
  
- **Perspectiva del Cliente** (2 KPIs):
  - Proyectos a tiempo
  - Proyectos cancelados
  
- **Perspectiva de Procesos Internos** (3 KPIs):
  - Tareas retrasadas
  - Hitos retrasados
  - Tasa de errores
  
- **Perspectiva de Aprendizaje** (3 KPIs):
  - Productividad
  - Tasa de éxito en pruebas
  - Relación horas

- **Visualizaciones**:
  - Presupuesto vs Real (barras)
  - Evolución de Entregas a Tiempo (línea temporal)
  - Productividad por Rol (barras)
  - Distribución CAPEX/OPEX (barras)

---

### 6.2 Vista 2: Análisis Detallado
**Función**: `render_detalle()`
**Archivo**: `dss/ui/views.py`

**Contenido**:

**Sección 1: Gestión Temporal**
- Retrasos de Inicio vs Finalización (barras comparativas)
- Duración Real vs Planificada (barras - calculada desde fechas)

**Sección 2: Gestión de Recursos Humanos**
- Productividad por Rol (relación horas reales/planificadas)
- Horas Planificadas vs Reales por Rol (barras agrupadas)

**Sección 3: Análisis Financiero**
- Desviación Presupuestal por Proyecto (barras)
- Penalizaciones vs Presupuesto (% sobre presupuesto)

**Sección 4: Métricas de Calidad**
- Total de Errores por Proyecto (barras)
- Tasa de Éxito en Pruebas (% convertido a escala 0-100)

**Tabla Detallada**:
- Filtrada según criterios del sidebar
- Columnas: Cliente, Proyecto, Presupuesto, Costo Real, Desviación, Retrasos, Productividad, KPIs de calidad

---

### 6.3 Vista 3: Métricas Calculadas
**Función**: `render_metricas_calculadas()`
**Archivo**: `dss/ui/views.py`

**Contenido**:

**Panel de Resumen** (4 métricas):
- Duración Promedio (días)
- Defectos Encontrados (total y promedio)
- Productividad Calculada
- Costo Real Promedio

**Análisis de Retrasos** (2 métricas con delta vs objetivo):
- Tareas Retrasadas (calculado vs 10% target)
- Hitos Retrasados (calculado vs 10% target)

**Tabla Detallada por Proyecto**:
- DuracionRealDias
- NumeroDefectosEncontrados
- ProductividadPromedio_Calculada
- PorcentajeTareasRetrasadas_Calculada
- PorcentajeHitosRetrasados_Calculada
- CostoReal_Horas
- CostoReal_Gastos
- CostoReal_Total_Calculado

**Explicaciones**: Cada métrica incluye tooltip con fórmula y fuentes de datos

---

### 6.4 Vista 4: Predicción de Defectos (Solo Project Managers)
**Función**: `render_prediccion()`
**Archivo**: `dss/ui/views.py`

**Contenido**:

**Panel de Entrada**:
- Duración estimada (días)
- Número de trabajadores
- Productividad esperada (slider 0-1)

**Predicción**:
- Número de defectos esperados
- Nivel de riesgo (BAJO/MEDIO/ALTO con colores)
- Métricas del modelo (MAE, RMSE, R²)

**Visualización**:
- Curva de Rayleigh (distribución temporal de defectos)
- Eje X: Días del proyecto
- Eje Y: Tasa de defectos esperada

**Recomendaciones Automáticas**:
- Lista de acciones según nivel de riesgo
- Plan de testing sugerido

**Proyectos Similares**:
- Tabla de proyectos históricos comparables
- Benchmarking de desempeño

---

## 🎨 7. DISEÑO DEL DASHBOARD

### 7.1 Características Visuales

**Estilo**: Formal y profesional (sin gradientes coloridos)

**Paleta de Colores**:
- Perspectiva Financiera: Verde (#11998e - #38ef7d)
- Perspectiva Cliente: Azul (#2980b9 - #6dd5fa)
- Perspectiva Procesos: Rojo/Rosa (#f857a6 - #ff5858)
- Perspectiva Aprendizaje: Amarillo/Rosa (#fa709a - #fee140)

**Componentes**:
- Tarjetas KPI con métricas y targets
- Gráficos nativos de Streamlit (sin plotly)
- Layout responsivo (2-4 columnas)
- Sin emojis ni elementos decorativos

### 7.2 Interactividad

**Filtros Sidebar**:
- Año de finalización (multiselect)
- Mes de finalización (multiselect)
- Cliente (multiselect)
- Proyecto (multiselect)
- Rol/Empleado (multiselect)

**Tabs de Navegación**:
1. Resumen general
2. Análisis detallado
3. Métricas Calculadas
4. Predicción de defectos (condicional)

**Actualización en Tiempo Real**:
- Cambios en filtros → Recálculo automático de KPIs
- Cache de datos para rendimiento
- Validaciones de existencia de columnas

---

## 🔧 8. ARQUITECTURA TÉCNICA

### 8.1 Stack Tecnológico

**Backend**:
- Python 3.x
- Pandas (manipulación de datos)
- NumPy (cálculos numéricos)
- SQLAlchemy (ORM para MySQL)
- SciPy (distribución de Rayleigh)
- Scikit-learn (modelo de regresión)

**Frontend**:
- Streamlit (framework web)
- Componentes nativos de Streamlit

**Base de Datos**:
- MySQL 8.x (producción)
- CSV (fallback)

### 8.2 Estructura de Archivos

```
Olguin_final/
├── app.py                          # Punto de entrada principal
├── requirements.txt                # Dependencias
├── README.md                       # Documentación
├── REPORTE_METRICAS_COMPLETO.md   # Este documento
├── CargaDatos/                     # Datos CSV
│   ├── hechos_proyectos_seed.csv
│   ├── hechos_asignaciones_seed.csv
│   ├── dim_proyectos_seed.csv
│   ├── dim_clientes_seed.csv
│   ├── dim_gastos_seed.csv
│   ├── dim_tiempo_seed.csv
│   ├── dim_empleados_seed.csv
│   ├── dim_hitos_seed.csv
│   ├── dim_tareas_seed.csv
│   └── dim_pruebas_seed.csv
└── dss/                            # Módulo principal
    ├── __init__.py
    ├── config.py                   # Configuración y targets de KPI
    ├── db.py                       # Conexión a MySQL
    ├── data_sources.py             # Carga de datos (CSV/MySQL)
    ├── analytics.py                # Cubo OLAP y KPIs
    ├── metricas_calculadas.py      # Métricas dinámicas
    ├── prediction.py               # Modelo Rayleigh
    ├── auth.py                     # Autenticación
    └── ui/                         # Interfaz de usuario
        ├── __init__.py
        ├── components.py           # Componentes reutilizables
        └── views.py                # Vistas del dashboard
```

### 8.3 Flujo de Datos

```
1. Usuario accede → Login (auth.py)
2. Carga de datos:
   - Intenta MySQL (db.py)
   - Fallback a CSV (data_sources.py)
   - Cache en memoria (@st.cache_data)
3. Usuario selecciona filtros → Sidebar
4. Operaciones OLAP:
   - aplicar_filtros() → SLICE/DICE
   - build_olap_views() → ROLL-UP/PIVOT
   - get_kpis() → Agregaciones
5. Renderizado:
   - Tabs selecciona vista
   - render_*() genera visualizaciones
   - Streamlit actualiza UI
6. Predicción (si PM):
   - Inputs usuario → prediction.py
   - Modelo Rayleigh → Curva + Recomendaciones
```

---

## 📈 9. CASOS DE USO

### 9.1 Caso de Uso 1: Análisis Mensual de Desempeño
**Actor**: Gerente de Operaciones

**Flujo**:
1. Accede al dashboard
2. Filtra por mes actual y año actual
3. Revisa Balanced Scorecard:
   - Identifica KPIs fuera de target (rojos)
   - Nota que "Tareas retrasadas" = 15% (target 10%)
4. Navega a "Análisis Detallado"
5. Revisa gráfico "Productividad por Rol"
   - Detecta que rol "QA" tiene relación 1.4 (40% sobre estimación)
6. Acción: Reunión con líder de QA para redistribuir carga

---

### 9.2 Caso de Uso 2: Planificación de Nuevo Proyecto
**Actor**: Project Manager

**Flujo**:
1. Accede a "Predicción de defectos"
2. Ingresa parámetros del nuevo proyecto:
   - Duración: 180 días
   - Trabajadores: 12
   - Productividad esperada: 0.75
3. Sistema predice:
   - 210 defectos esperados → RIESGO ALTO
   - Pico de defectos: día 126
4. Revisa recomendaciones:
   - "Reforzar equipo de QA en 30%"
   - "Cobertura de código mínima: 80%"
5. Consulta proyectos similares
6. Ajusta plan:
   - Contrata 2 QA adicionales
   - Planifica testing intensivo semana 18-20

---

### 9.3 Caso de Uso 3: Revisión de Métricas Calculadas
**Actor**: Analista de Datos

**Flujo**:
1. Navega a "Métricas Calculadas"
2. Revisa estadísticas globales:
   - Duración promedio: 165 días
   - Defectos totales: 550 (promedio 137 por proyecto)
3. Filtra por cliente específico (501)
4. Compara métricas calculadas vs precalculadas:
   - Productividad calculada: 18.3 días/empleado
   - Productividad precalculada (hechos): 0.78
5. Identifica discrepancia
6. Investiga fuente de datos
7. Documenta hallazgos para equipo de data warehouse

---

### 9.4 Caso de Uso 4: Drill-Down en Proyectos Retrasados
**Actor**: Director de Proyectos

**Flujo**:
1. En BSC, observa KPI "Proyectos a tiempo" = 70% (bajo del 85% target)
2. Navega a "Análisis Detallado"
3. Revisa gráfico "Retrasos de Inicio vs Finalización"
4. Identifica proyectos con >15 días de retraso final
5. Aplica filtro por esos proyectos específicos
6. Revisa tabla detallada:
   - Proyecto 1003: Retraso 15 días, Desviación +50K, Errores 200
7. Acciones:
   - Escalamiento a equipo ejecutivo
   - Revisión de plan de mitigación

---

## 🎓 10. CONCLUSIONES Y MEJORES PRÁCTICAS

### 10.1 Fortalezas del Sistema

1. **Integración completa**: KPIs → Métricas → OLAP → Predicción
2. **Flexibilidad**: Funciona con MySQL o CSV
3. **Escalabilidad**: Cache inteligente para grandes volúmenes
4. **Usabilidad**: Interfaz intuitiva sin curva de aprendizaje
5. **Precisión**: Métricas calculadas en tiempo real vs precalculadas

### 10.2 Recomendaciones de Uso

**Para Ejecutivos**:
- Revisar BSC semanalmente
- Enfocarse en KPIs rojos (fuera de target)
- Comparar tendencias mes a mes

**Para Project Managers**:
- Usar predicción Rayleigh al inicio de cada proyecto
- Monitorear métricas calculadas durante ejecución
- Ajustar plan según recomendaciones automáticas

**Para Analistas**:
- Validar coherencia entre métricas calculadas y precalculadas
- Documentar discrepancias en data warehouse
- Sugerir nuevas dimensiones/métricas según necesidades

### 10.3 Limitaciones Conocidas

1. **Modelo Rayleigh**: Asume distribución normal de defectos (no siempre real)
2. **Datos históricos**: Predicción requiere al menos 10-15 proyectos similares
3. **Granularidad temporal**: Dimensión tiempo no incluye día de la semana
4. **Métricas de satisfacción**: No incluye NPS o feedback directo de clientes

### 10.4 Roadmap Futuro

**Corto plazo (1-3 meses)**:
- [ ] Agregar alertas automáticas por email
- [ ] Dashboard móvil (responsive design mejorado)
- [ ] Exportación de reportes a PDF

**Mediano plazo (3-6 meses)**:
- [ ] Integración con Jira/Azure DevOps
- [ ] Machine Learning para predicción de retrasos
- [ ] Dashboard de costos en tiempo real

**Largo plazo (6-12 meses)**:
- [ ] Migración a cubo MOLAP (Microsoft Analysis Services)
- [ ] BI embebido en aplicaciones de gestión
- [ ] Análisis de sentimiento de feedback de clientes

---

## 📞 SOPORTE Y CONTACTO

**Documentación técnica**: `README.md`, `MEJORAS_PREDICCION.md`, `ANALISIS_METRICAS.md`

**Usuarios de prueba**:
- Project Manager: `pm1` / `1234`
- Analista: `analista1` / `abcd`

**Base de datos**: `dw_proyectos` (MySQL 3307)

**Ejecución**: `streamlit run app.py`

---

*Documento generado el 22 de noviembre de 2025*  
*Versión del sistema: 1.0*  
*Proyecto: DSS - Dashboard de Desempeño de Proyectos de Software*
