"""
Configuración y gestión de conexión a la base de datos TiDB Cloud
"""
import os
import pymysql
import pandas as pd
from dotenv import load_dotenv
from typing import Optional
import streamlit as st

# Cargar variables de entorno
load_dotenv()

class DatabaseConfig:
    """Configuración de conexión a TiDB Cloud"""
    
    def __init__(self):
        self.host = os.getenv("DW_HOST")
        self.port = int(os.getenv("DW_PORT", 4000))
        self.user = os.getenv("DW_USER")
        self.password = os.getenv("DW_PASS")
        self.database = os.getenv("DW_DB")
        self.ssl = os.getenv("DW_SSL", "true").lower() == "true"
    
    def validate(self) -> bool:
        """Valida que todas las credenciales estén presentes"""
        required = [self.host, self.user, self.password, self.database]
        return all(required)


@st.cache_resource
def get_database_connection():
    """
    Crea y retorna una conexión a TiDB Cloud
    Usa caché de Streamlit para mantener la conexión activa
    """
    config = DatabaseConfig()
    
    if not config.validate():
        raise ValueError("Configuración de base de datos incompleta. Verifica el archivo .env")
    
    try:
        connection = pymysql.connect(
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.password,
            database=config.database,
            ssl={'ssl': config.ssl} if config.ssl else None,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=10,
            read_timeout=30,
            write_timeout=30
        )
        return connection
    except Exception as e:
        raise ConnectionError(f"Error conectando a TiDB Cloud: {str(e)}")


def execute_query(query: str, params: Optional[tuple] = None) -> pd.DataFrame:
    """
    Ejecuta una query SQL y retorna los resultados como DataFrame
    
    Args:
        query: Query SQL a ejecutar
        params: Parámetros para la query (opcional)
    
    Returns:
        DataFrame con los resultados
    """
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        
        # Ejecutar query
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Obtener resultados
        rows = cursor.fetchall()
        
        # Convertir a DataFrame
        if rows:
            df = pd.DataFrame(rows)
        else:
            # Si no hay resultados, crear DataFrame vacío con las columnas correctas
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            df = pd.DataFrame(columns=columns)
        
        cursor.close()
        return df
    
    except Exception as e:
        st.error(f"Error ejecutando query: {str(e)}")
        raise


def test_connection() -> bool:
    """
    Prueba la conexión a la base de datos
    
    Returns:
        True si la conexión es exitosa, False en caso contrario
    """
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            return result['test'] == 1
    except Exception as e:
        print(f"Error en test de conexión: {str(e)}")
        return False


def get_table_info(table_name: str) -> pd.DataFrame:
    """
    Obtiene información sobre las columnas de una tabla
    
    Args:
        table_name: Nombre de la tabla
    
    Returns:
        DataFrame con información de las columnas
    """
    query = f"""
    SELECT 
        COLUMN_NAME as columna,
        DATA_TYPE as tipo,
        IS_NULLABLE as nullable,
        COLUMN_KEY as clave
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
    ORDER BY ORDINAL_POSITION
    """
    
    config = DatabaseConfig()
    return execute_query(query, (config.database, table_name))


def get_available_tables() -> list:
    """
    Obtiene la lista de tablas disponibles en la base de datos
    
    Returns:
        Lista de nombres de tablas
    """
    query = """
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = %s AND TABLE_TYPE = 'BASE TABLE'
    ORDER BY TABLE_NAME
    """
    
    config = DatabaseConfig()
    df = execute_query(query, (config.database,))
    return df['TABLE_NAME'].tolist()


# Queries predefinidas para las tablas del Data Warehouse
QUERIES = {
    "hechos_proyectos": """
        SELECT * FROM hechos_proyectos
    """,
    
    "dim_proyectos": """
        SELECT * FROM dim_proyectos
    """,
    
    "dim_clientes": """
        SELECT * FROM dim_clientes
    """,
    
    "dim_tiempo": """
        SELECT * FROM dim_tiempo
    """,
    
    "dim_equipo": """
        SELECT * FROM dim_equipo
    """,
    
    "dim_tecnologias": """
        SELECT * FROM dim_tecnologias
    """,
    
    # Query completa con todos los JOINs
    "hechos_completos": """
        SELECT 
            h.*,
            p.NombreProyecto,
            p.DescripcionProyecto,
            c.NombreCliente,
            c.TipoIndustria,
            ti.Anio,
            ti.Mes,
            ti.NombreMes,
            ti.Trimestre,
            e.TamanoEquipo,
            e.ExperienciaPromedio,
            tec.TecnologiasPrincipales,
            tec.FrameworksUtilizados
        FROM hechos_proyectos h
        LEFT JOIN dim_proyectos p ON h.ProyectoID = p.ProyectoID
        LEFT JOIN dim_clientes c ON h.ClienteID = c.ClienteID
        LEFT JOIN dim_tiempo ti ON h.TiempoID = ti.TiempoID
        LEFT JOIN dim_equipo e ON h.EquipoID = e.EquipoID
        LEFT JOIN dim_tecnologias tec ON h.TecnologiaID = tec.TecnologiaID
    """
}


def get_hechos_proyectos_completo() -> pd.DataFrame:
    """
    Obtiene la tabla de hechos con todas las dimensiones mediante JOINs
    Similar a como estaba en CSV pero desde BD
    
    Returns:
        DataFrame con todos los datos combinados
    """
    return execute_query(QUERIES["hechos_completos"])


def get_hechos_proyectos() -> pd.DataFrame:
    """
    Obtiene solo la tabla de hechos
    
    Returns:
        DataFrame con hechos de proyectos
    """
    return execute_query(QUERIES["hechos_proyectos"])


def get_dimension(dimension_name: str) -> pd.DataFrame:
    """
    Obtiene una tabla de dimensión específica
    
    Args:
        dimension_name: Nombre de la dimensión (proyectos, clientes, tiempo, equipo, tecnologias)
    
    Returns:
        DataFrame con la dimensión solicitada
    """
    table_name = f"dim_{dimension_name}"
    if table_name in QUERIES:
        return execute_query(QUERIES[table_name])
    else:
        raise ValueError(f"Dimensión '{dimension_name}' no encontrada")
