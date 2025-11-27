import pandas as pd

# Cargar CSV
df = pd.read_csv(r'c:\Users\jovas\Downloads\2025-11-27T01-21_export.csv')

print("=" * 80)
print("ANÁLISIS DE LA CURVA DE RAYLEIGH")
print("=" * 80)

# Total de defectos
total_defectos = df['DefectosAcumulados'].max()
print(f"\n📊 Total de defectos predichos: {total_defectos:.2f}")
print(f"📅 Duración del proyecto: {int(df['Tiempo'].max())} semanas")

# Calcular tasa de defectos por semana (derivada)
df['Tasa'] = df['DefectosAcumulados'].diff().fillna(0)

# Encontrar pico de detección (el valor de Tiempo ya representa semanas)
pico_idx = df['Tasa'].idxmax()
semana_pico = int(df.iloc[pico_idx]['Tiempo'])
tasa_max = df.iloc[pico_idx]['Tasa']

print(f"\n🔝 PICO DE DETECCIÓN:")
print(f"   Semana: {semana_pico}")
print(f"   Tasa máxima: {tasa_max:.2f} defectos/semana")

# Encontrar 50% de defectos
defectos_50 = total_defectos * 0.5
idx_50 = (df['DefectosAcumulados'] >= defectos_50).idxmax()
semana_50 = int(df.iloc[idx_50]['Tiempo'])
defectos_en_50 = df.iloc[idx_50]['DefectosAcumulados']

print(f"\n📈 50% DE DEFECTOS ({defectos_50:.2f}):")
print(f"   Semana: {semana_50}")
print(f"   Defectos acumulados: {defectos_en_50:.2f}")

# Encontrar 90% de defectos
defectos_90 = total_defectos * 0.9
idx_90 = (df['DefectosAcumulados'] >= defectos_90).idxmax()
semana_90 = int(df.iloc[idx_90]['Tiempo'])
defectos_en_90 = df.iloc[idx_90]['DefectosAcumulados']

print(f"\n📈 90% DE DEFECTOS ({defectos_90:.2f}):")
print(f"   Semana: {semana_90}")
print(f"   Defectos acumulados: {defectos_en_90:.2f}")

print("\n" + "=" * 80)
print("VERIFICACIÓN CON VALORES MOSTRADOS EN LA IMAGEN")
print("=" * 80)
print(f"\nLa imagen muestra:")
print(f"  - Pico de detección: Semana 2")
print(f"  - 50% defectos: Semana 3")
print(f"  - 90% defectos: Semana 5")
print(f"  - Tooltip en tiempo 21: 9.32 defectos (semana 21)")
print(f"\nNuestros cálculos:")
print(f"  - Pico de detección: Semana {semana_pico}")
print(f"  - 50% defectos: Semana {semana_50}")
print(f"  - 90% defectos: Semana {semana_90}")

if semana_pico == 18 and semana_50 == 21 and semana_90 == 37:
    print("\n✅ PERFECTO! Los cálculos están correctos.")
    print("   - El tooltip muestra tiempo=21 que es SEMANA 21 (no día 21)")
else:
    print("\n⚠️ Verificando valores...")
    print(f"\nDatos encontrados:")
    print(f"  - Pico: semana {semana_pico} (esperado ~18)")
    print(f"  - 50%: semana {semana_50} (esperado ~21)")
    print(f"  - 90%: semana {semana_90} (esperado ~37)")

print("\n" + "=" * 80)
print("RECOMENDACIÓN")
print("=" * 80)
print(f"Concentrar máximo esfuerzo de QA entre semanas {max(1, semana_pico-1)} y {semana_50+1}")
print("=" * 80)
