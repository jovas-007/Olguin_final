"""Script de test para verificar carga de métricas"""
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "CargaDatos"

# Cargar tablas
print("=== CARGANDO DATOS ===")
hechos = pd.read_csv(DATA_DIR / "hechos_proyectos_seed.csv")
dim_proyectos = pd.read_csv(DATA_DIR / "dim_proyectos_seed.csv")
dim_clientes = pd.read_csv(DATA_DIR / "dim_clientes_seed.csv")
dim_tiempo = pd.read_csv(DATA_DIR / "dim_tiempo_seed.csv")

print(f"\nHechos proyectos: {len(hechos)} filas")
print(f"Columnas hechos: {hechos.columns.tolist()}")

print(f"\nDim proyectos: {len(dim_proyectos)} filas")
print(f"Columnas dim_proyectos: {dim_proyectos.columns.tolist()}")

# Seleccionar columnas de métricas
columnas_metricas = [
    "ID_Proyecto",
    "RetrasoInicioDias",
    "RetrasoFinalDias",
    "Presupuesto",
    "CosteReal",
    "DesviacionPresupuestal",
    "PenalizacionesMonto",
    "ProporcionCAPEX_OPEX",
    "TasaDeErroresEncontrados",
    "TasaDeExitoEnPruebas",
    "ProductividadPromedio",
    "PorcentajeTareasRetrasadas",
    "PorcentajeHitosRetrasados",
]

columnas_existentes = [col for col in columnas_metricas if col in hechos.columns]
print(f"\nColumnas de métricas encontradas: {columnas_existentes}")

df_metricas = hechos[columnas_existentes].copy()
print(f"\nDataFrame métricas shape: {df_metricas.shape}")
print(f"\nPrimeras 3 filas:\n{df_metricas.head(3)}")

# Hacer merge con dim_proyectos
print("\n=== MERGE CON DIM_PROYECTOS ===")
df_proyectos_info = dim_proyectos[["ID_Proyecto", "CodigoProyecto"]].copy()
df_completo = df_metricas.merge(df_proyectos_info, on="ID_Proyecto", how="left")

print(f"DataFrame completo shape: {df_completo.shape}")
print(f"Columnas: {df_completo.columns.tolist()}")
print(f"\nPrimeras 3 filas:\n{df_completo.head(3)}")

# Verificar CodigoProyecto
print(f"\n¿Tiene CodigoProyecto? {'CodigoProyecto' in df_completo.columns}")
print(f"Valores únicos CodigoProyecto: {df_completo['CodigoProyecto'].nunique()}")

# Test de visualización
print("\n=== TEST VISUALIZACIÓN ===")
if "CodigoProyecto" in df_completo.columns and "RetrasoInicioDias" in df_completo.columns:
    chart_data = df_completo[["CodigoProyecto", "RetrasoInicioDias"]].set_index("CodigoProyecto").head(5)
    print("Datos para gráfico Retrasos:")
    print(chart_data)
else:
    print("ERROR: Faltan columnas para visualización")

if "CodigoProyecto" in df_completo.columns and "Presupuesto" in df_completo.columns and "CosteReal" in df_completo.columns:
    chart_data2 = df_completo[["CodigoProyecto", "Presupuesto", "CosteReal"]].set_index("CodigoProyecto").head(5)
    print("\nDatos para gráfico Presupuesto vs Costo:")
    print(chart_data2)
else:
    print("ERROR: Faltan columnas para visualización financiera")
