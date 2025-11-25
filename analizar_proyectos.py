import pandas as pd

# Cargar datos
df_p = pd.read_csv('CargaDatos/dim_proyectos_seed.csv')
df_h = pd.read_csv('CargaDatos/hechos_proyectos_seed.csv')
df = pd.merge(df_p, df_h, on='ID_Proyecto')

# Buscar grupos de proyectos similares
print("=" * 80)
print("ANÁLISIS DE PROYECTOS PARA PREDICCIÓN")
print("=" * 80)

# Proyectos con presupuesto alrededor de $150,000
grupo1 = df[(df['Presupuesto'] >= 105000) & (df['Presupuesto'] <= 195000)]
print(f"\n📊 GRUPO 1: Presupuesto entre $105K - $195K ({len(grupo1)} proyectos)")
print(grupo1[['CodigoProyecto', 'Presupuesto', 'NumTrabajadores', 'TotalErrores', 'RetrasoFinalDias']].head(10))

if len(grupo1) >= 3:
    promedio = grupo1.iloc[0]
    print(f"\n✅ EJEMPLO RECOMENDADO #1:")
    print(f"   Presupuesto: ${promedio['Presupuesto']:,.2f}")
    print(f"   Trabajadores: {promedio['NumTrabajadores']}")
    print(f"   (Encontrará {len(grupo1)} proyectos similares)")

# Proyectos con presupuesto alrededor de $200,000
grupo2 = df[(df['Presupuesto'] >= 140000) & (df['Presupuesto'] <= 260000)]
print(f"\n📊 GRUPO 2: Presupuesto entre $140K - $260K ({len(grupo2)} proyectos)")
print(grupo2[['CodigoProyecto', 'Presupuesto', 'NumTrabajadores', 'TotalErrores', 'RetrasoFinalDias']].head(10))

if len(grupo2) >= 3:
    promedio = grupo2.iloc[0]
    print(f"\n✅ EJEMPLO RECOMENDADO #2:")
    print(f"   Presupuesto: ${promedio['Presupuesto']:,.2f}")
    print(f"   Trabajadores: {promedio['NumTrabajadores']}")
    print(f"   (Encontrará {len(grupo2)} proyectos similares)")

# Proyectos pequeños
grupo3 = df[(df['Presupuesto'] >= 66500) & (df['Presupuesto'] <= 123500)]
print(f"\n📊 GRUPO 3: Presupuesto entre $66.5K - $123.5K ({len(grupo3)} proyectos)")
print(grupo3[['CodigoProyecto', 'Presupuesto', 'NumTrabajadores', 'TotalErrores', 'RetrasoFinalDias']].head(10))

if len(grupo3) >= 3:
    promedio = grupo3.iloc[0]
    print(f"\n✅ EJEMPLO RECOMENDADO #3:")
    print(f"   Presupuesto: ${promedio['Presupuesto']:,.2f}")
    print(f"   Trabajadores: {promedio['NumTrabajadores']}")
    print(f"   (Encontrará {len(grupo3)} proyectos similares)")

print("\n" + "=" * 80)
print("CONFIGURACIONES RECOMENDADAS PARA DEMO:")
print("=" * 80)
print("\nPara ver proyectos similares, usa estos valores:\n")

ejemplos = [
    {"Presupuesto": 150000, "Trabajadores": 25, "Duracion": 60, "Descripcion": "Proyecto mediano estándar"},
    {"Presupuesto": 200000, "Trabajadores": 28, "Duracion": 75, "Descripcion": "Proyecto grande"},
    {"Presupuesto": 95000, "Trabajadores": 24, "Duracion": 50, "Descripcion": "Proyecto pequeño"},
]

for i, ej in enumerate(ejemplos, 1):
    pmin = ej['Presupuesto'] * 0.7
    pmax = ej['Presupuesto'] * 1.3
    tmin = ej['Trabajadores'] - 2
    tmax = ej['Trabajadores'] + 2
    
    similares = df[
        (df["Presupuesto"] >= pmin) &
        (df["Presupuesto"] <= pmax) &
        (df["NumTrabajadores"] >= tmin) &
        (df["NumTrabajadores"] <= tmax)
    ]
    
    print(f"\n{i}. {ej['Descripcion']}:")
    print(f"   • Presupuesto: ${ej['Presupuesto']:,}")
    print(f"   • Trabajadores: {ej['Trabajadores']}")
    print(f"   • Duración: {ej['Duracion']} semanas")
    print(f"   • Complejidad: media")
    print(f"   ➜ Mostrará {len(similares)} proyectos similares ✓")
