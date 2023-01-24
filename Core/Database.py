import sqlite3 as sql
db_name = "Registro.db"

def createDB():
    conn = sql.connect(db_name)
    conn.commit()
    conn.close()

def run_query(query, parametros = ()):
    with sql.connect(db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parametros)
        conn.commit()
    return result

def createTableMaterias():
    run_query("""CREATE TABLE IF NOT EXISTS Materias (
        Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        Materia text)""")

def createTableCantidad():
    run_query("""CREATE TABLE IF NOT EXISTS Cantidad (
        Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        Fecha text, 
        cantidad text)""")

def createTableConfig():
    run_query("""
        CREATE TABLE IF NOT EXISTS Configuracion (
            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Nombres text, 
            Apellidos text,
            Paralelo text,
            Ruta text)""")

def createTableNotas():
    run_query("""
        CREATE TABLE IF NOT EXISTS Notas (
            id INTEGER PRIMARY KEY,
            dia INTEGER,
            mes INTEGER,
            año INTEGER,
            descripcion TEXT,
            prioridad TEXT
            )""")


def insert_db(dia, mes, año, descripcion, prioridad):
    run_query("INSERT INTO Notas VALUES (NULL, ?, ?, ?, ?, ?)", (dia, mes, año, descripcion, prioridad))


def delete_Nota(id):
    run_query("DELETE FROM Notas WHERE id = ?", (id,))
 

def search_DayData(**kwargs):
    Id = kwargs.get('Id', None)
    if Id:
        rows = run_query("SELECT * FROM Notas WHERE id = ?", (Id,)).fetchone()
        return rows if len(rows) != 0 else None
    else:
        dia = kwargs.get('dia', None)
        mes = kwargs.get('mes', None)
        año = kwargs.get('año', None)
        rows = run_query("SELECT * FROM Notas WHERE dia = ? AND mes = ? AND año = ?", (dia, mes, año)).fetchall()
        return rows if len(rows) != 0 else None