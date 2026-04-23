# ==== NEGOCIO ====

from data import get_all_data


def get_db_description():
    """
    Devuelve una descripción estructurada de la base de datos
    """
    df = get_all_data()

    columnas = {}
    for col in df.columns:
        columnas[col] = str(df[col].dtype)

    return {
        "tabla": "accidentes",
        "total_columnas": len(df.columns),
        "columnas": columnas
    }


def describe_table():
    """
    Simula un DESCRIBE SQL real
    """
    df = get_all_data()

    descripcion = []

    for col in df.columns:
        descripcion.append({
            "columna": col,
            "tipo": str(df[col].dtype),
            "nulos": int(df[col].isnull().sum())
        })

    return descripcion


def preview_schema(n=5):
    """
    Muestra un preview de la tabla (tipo SELECT * LIMIT n)
    """
    df = get_all_data()
    return df.head(n)


def get_column_info(col_name):
    """
    Información específica de una columna
    """
    df = get_all_data()

    if col_name not in df.columns:
        return f"Columna '{col_name}' no existe"

    return {
        "columna": col_name,
        "tipo": str(df[col_name].dtype),
        "valores_unicos": int(df[col_name].nunique()),
        "nulos": int(df[col_name].isnull().sum())
    }