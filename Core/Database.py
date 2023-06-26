import sqlite3 as sql

class Query(object):
    def __init__(self) -> None:
        self.database = "database.db"
    
    def createDB(self):
        conn = sql.connect(self.database)
        conn.commit()
        conn.close()
        
        self.createTables()


    def run_query(self,query, parametros = ()):
        with sql.connect(self.database) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parametros)
            conn.commit()
        return result

        
    def createTables(self):
        tables = [
            "CREATE TABLE IF NOT EXISTS Materia (Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Materia text)",
            "CREATE TABLE IF NOT EXISTS Tarea (Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Fecha text, Materia text)",
            "CREATE TABLE IF NOT EXISTS Configuracion (Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Nombres text, Apellidos text, Paralelo text, Ruta text)",
            "CREATE TABLE IF NOT EXISTS Nota (id INTEGER PRIMARY KEY, dia INTEGER, mes INTEGER, año INTEGER, descripcion TEXT, prioridad TEXT)"
        ]
        for table in tables:
            self.run_query(table)    
        
    def insert_db(self, dia, mes, año, descripcion, prioridad):
        self.run_query("INSERT INTO Notas VALUES (NULL, ?, ?, ?, ?, ?)", (dia, mes, año, descripcion, prioridad))


    def delete_Nota(self, id):
        self.run_query("DELETE FROM Notas WHERE id = ?", (id,))
    

    def search_DayData(self, **kwargs):
        Id = kwargs.get('Id', None)
        if Id:
            rows = self.run_query("SELECT * FROM Notas WHERE id = ?", (Id,)).fetchone()
            return rows if len(rows) != 0 else None
        else:
            dia = kwargs.get('dia', None)
            mes = kwargs.get('mes', None)
            año = kwargs.get('año', None)
            rows = self.run_query("SELECT * FROM Notas WHERE dia = ? AND mes = ? AND año = ?", (dia, mes, año)).fetchall()
            return rows if len(rows) != 0 else None
        
    def getMaterias(self):
        return self.run_query("SELECT Materia FROM Materia").fetchall()