import sqlite3 as sql
db_name = "Asistencia.db"

def createDB():
    conn = sql.connect(db_name)
    conn.commit()
    conn.close()
def createTableMaterias():
    conn = sql.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Materias (
            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Materia text)"""
    )
    conn.commit()
    conn.close()
def createTableCantidad():
    conn = sql.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Cantidad (
            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Fecha text, 
            cantidad text)""")
    conn.commit()
    conn.close()
def createTableConfig():
    conn = sql.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Configuracion (
            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Nombres text, 
            Apellidos text,
            Paralelo text,
            Ruta text)""")
    conn.commit()
    conn.close()
def run_query(query, parametros = ()):
    with sql.connect(db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parametros)
        conn.commit()
    return result

