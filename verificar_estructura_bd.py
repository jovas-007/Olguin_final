"""
Verificar la estructura real de las tablas en la BD
"""
from dss.db_config import get_database_connection

conn = get_database_connection()
cursor = conn.cursor()

print("=" * 80)
print("ESTRUCTURA DE LA BASE DE DATOS")
print("=" * 80)

# Verificar hechos_proyectos
print("\n1. Tabla: hechos_proyectos")
cursor.execute("SELECT * FROM hechos_proyectos LIMIT 5")
rows = cursor.fetchall()
print(f"   Registros obtenidos: {len(rows)}")
if rows:
    print(f"   Primer registro:")
    for key, value in rows[0].items():
        print(f"     {key}: {value}")
    print(f"\n   Segundo registro:")
    if len(rows) > 1:
        for key, value in rows[1].items():
            print(f"     {key}: {value}")

# Verificar dim_proyectos
print("\n2. Tabla: dim_proyectos")
cursor.execute("SELECT * FROM dim_proyectos LIMIT 3")
rows = cursor.fetchall()
print(f"   Registros obtenidos: {len(rows)}")
if rows:
    print(f"   Primer registro:")
    for key, value in rows[0].items():
        print(f"     {key}: {value}")

# Verificar dim_clientes
print("\n3. Tabla: dim_clientes")
cursor.execute("SELECT * FROM dim_clientes LIMIT 3")
rows = cursor.fetchall()
print(f"   Registros obtenidos: {len(rows)}")
if rows:
    print(f"   Primer registro:")
    for key, value in rows[0].items():
        print(f"     {key}: {value}")

# Contar registros reales vs headers
print("\n" + "=" * 80)
print("ANÁLISIS DE DATOS")
print("=" * 80)

cursor.execute("""
    SELECT ID_Proyecto, Presupuesto, CosteReal 
    FROM hechos_proyectos 
    WHERE ID_Proyecto != 'ID_Proyecto'
    LIMIT 5
""")
rows = cursor.fetchall()
print(f"\n✅ Registros VÁLIDOS (excluyendo headers): {len(rows)}")
if rows:
    for row in rows:
        print(f"   {row}")

conn.close()
