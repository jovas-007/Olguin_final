from dss.db_config import execute_query

tablas = ['hechos_proyectos', 'hechos_asignaciones', 'dim_proyectos']

for tabla in tablas:
    result = execute_query(f'SELECT COUNT(*) as total FROM {tabla}')
    print(f'{tabla}:')
    print(result)
    print()
