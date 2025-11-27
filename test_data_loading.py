"""
Script para verificar que la carga de datos desde BD funciona correctamente
"""
import sys
import pandas as pd

# Deshabilitar Streamlit
import os
os.environ["STREAMLIT_DISABLE"] = "1"

from dss.data_sources import cargar_df_proyectos, cargar_df_asignaciones

print("=" * 80)
print("PRUEBA DE CARGA DE DATOS DESDE BASE DE DATOS")
print("=" * 80)

# Test 1: Cargar proyectos
print("\n1. Cargando proyectos desde BD...")
try:
    df_proyectos = cargar_df_proyectos()
    print(f"✅ Proyectos cargados: {len(df_proyectos)} registros")
    print(f"\nColumnas disponibles ({len(df_proyectos.columns)}):")
    for i, col in enumerate(df_proyectos.columns, 1):
        print(f"  {i:2d}. {col}")
    
    if len(df_proyectos) > 0:
        print(f"\n📊 Primeros 3 proyectos:")
        print(df_proyectos[['ID_Proyecto', 'CodigoProyecto', 'CodigoClienteReal', 'Presupuesto', 'CosteReal']].head(3).to_string())
        
        print(f"\n📈 Estadísticas básicas:")
        print(f"  - Presupuesto promedio: ${df_proyectos['Presupuesto'].mean():,.2f}")
        print(f"  - Coste real promedio: ${df_proyectos['CosteReal'].mean():,.2f}")
        print(f"  - Proyectos cancelados: {df_proyectos['Cancelado'].sum()}")
        print(f"  - Clientes únicos: {df_proyectos['CodigoClienteReal'].nunique()}")
    else:
        print("⚠️ No se encontraron proyectos!")
        
except Exception as e:
    print(f"❌ Error al cargar proyectos: {str(e)}")
    import traceback
    traceback.print_exc()

# Test 2: Cargar asignaciones
print("\n" + "=" * 80)
print("2. Cargando asignaciones desde BD...")
try:
    df_asignaciones = cargar_df_asignaciones()
    print(f"✅ Asignaciones cargadas: {len(df_asignaciones)} registros")
    print(f"\nColumnas disponibles ({len(df_asignaciones.columns)}):")
    for i, col in enumerate(df_asignaciones.columns, 1):
        print(f"  {i:2d}. {col}")
    
    if len(df_asignaciones) > 0:
        print(f"\n📊 Primeras 3 asignaciones:")
        print(df_asignaciones[['ID_Empleado', 'CodigoEmpleado', 'Rol', 'HorasPlanificadas', 'HorasReales']].head(3).to_string())
        
        print(f"\n📈 Estadísticas básicas:")
        print(f"  - Horas planificadas totales: {df_asignaciones['HorasPlanificadas'].sum():,.2f}")
        print(f"  - Horas reales totales: {df_asignaciones['HorasReales'].sum():,.2f}")
        print(f"  - Empleados únicos: {df_asignaciones['ID_Empleado'].nunique()}")
        print(f"  - Proyectos con asignaciones: {df_asignaciones['ID_Proyecto'].nunique()}")
    else:
        print("⚠️ No se encontraron asignaciones!")
        
except Exception as e:
    print(f"❌ Error al cargar asignaciones: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("PRUEBA COMPLETADA")
print("=" * 80)
