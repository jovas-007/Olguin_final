"""
Probar el query JOIN directamente
"""
from dss.db_config import get_database_connection
import pandas as pd

conn = get_database_connection()

query = """
SELECT 
    hp.ID_Proyecto,
    dp.CodigoProyecto,
    dp.Version,
    dp.Cancelado,
    hp.Presupuesto,
    hp.CosteReal,
    dc.CodigoClienteReal
FROM hechos_proyectos hp
LEFT JOIN dim_proyectos dp ON hp.ID_Proyecto = dp.ID_Proyecto
LEFT JOIN dim_clientes dc ON dp.ID_Cliente = dc.ID_Cliente
LIMIT 5
"""

print("=" * 80)
print("QUERY JOIN TEST")
print("=" * 80)

# Test con cursor
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()

print(f"\n✅ Registros obtenidos con cursor: {len(rows)}")
if rows:
    print("\nPrimer registro (cursor):")
    for key, value in rows[0].items():
        print(f"  {key}: {value} (tipo: {type(value).__name__})")

# Test con pandas
print("\n" + "=" * 80)
df = pd.read_sql(query, conn)
print(f"✅ DataFrame shape: {df.shape}")
print(f"\nColumnas: {list(df.columns)}")
print(f"\nPrimeras 3 filas:")
print(df.head(3))

print(f"\nTipos de datos:")
print(df.dtypes)

conn.close()
