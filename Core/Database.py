import sqlite3 as sql
import os
import random

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
            "CREATE TABLE IF NOT EXISTS Tarea (Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Materia text, Documento text, Numero int, FechaHora datetime)",
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
        
    def getMateriasList(self):
        Materias = self.run_query("SELECT Materia FROM Materia").fetchall()
        return [i[0] for i in Materias]
    
    def deleteMateria(self, materia):
        self.run_query("DELETE FROM Materia WHERE Materia = ?", (materia,))
        
    def getHomeworksPath(self):
        Path = self.run_query("SELECT Ruta FROM Configuracion").fetchone()
        Path = Path[0] if Path else os.getcwd()
        return Path

    def getConfigData(self):
        DatosConfig = self.query.run_query("SELECT * FROM Configuracion").fetchone()
        return DatosConfig

    def getHomeworksList(self, fecha = None):
        if not fecha:
            return self.run_query("SELECT * FROM Tarea").fetchall()
        return self.run_query("SELECT * FROM Tarea WHERE Fecha = ?", (fecha,)).fetchall()
    
    def createHomework(self, fecha, materia):
        self.run_query("INSERT INTO Tarea VALUES (NULL, ?, ?)", (fecha, materia))
        
    

    def createFakeHomeworks(self):
        import random
        import string
        from datetime import datetime, timedelta

        def generar_registros(num_registros):
            registros = []
            fecha_actual = datetime.now()

            for _ in range(num_registros):
                cantidad = random.randint(1, 5)
                Materias = ["Lenguaje", "Matematicas avanzadas", "Ciencias Naturales", "Fisica", "Desarrollo de Software", "Programacion"]
                for _ in range(cantidad):
                    materia = ''.join(random.choices(Materias, k=1))
                    documento = "Documento " + ''.join(random.choices(string.ascii_uppercase, k=2))
                    
                    fecha_hora = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
                    # change the hour values 

                    hora = random.randint(0, 23)
                    hora = str(hora).zfill(2)  # Agrega un cero inicial si es necesario

                    minutos = random.randint(0, 59)
                    minutos = str(minutos).zfill(2)  # Agrega un cero inicial si es necesario

                    segundos = random.randint(0, 59)
                    segundos = str(segundos).zfill(2)  # Agrega un cero inicial si es necesario

                    
                    
                    
                    fecha_hora = fecha_hora.split(" ")[0] + " " + hora + ":" + minutos + ":" + segundos


                    obj = {}
                    for registro in registros:
                        materiac, documentoc, numeroc, fecha_horac = registro
                        Fecha = datetime.strptime(fecha_horac, "%Y-%m-%d %H:%M:%S")
                        Fecha = Fecha.strftime("%Y-%m-%d")
                        obj[f"{Fecha}-{materiac}"] = obj.get(f"{Fecha}-{materiac}", 0) + 1
                        

                    Fecha = fecha_hora.split(" ")[0]
                    numero = obj.get(f"{Fecha}-{materia}", 0) + 1

                    
                    registros.append((materia, documento, numero, fecha_hora))

                fecha_actual += timedelta(days=1)

            return registros
        

        registros = generar_registros(100)

        for registro in registros:
            query = "INSERT INTO Tarea (Materia, Documento, Numero, FechaHora) VALUES (?, ?, ?, ?)"
            self.run_query(query, registro)
        Materias = ["Lenguaje", "Matematicas avanzadas", "Ciencias Naturales", "Fisica", "Desarrollo de Software", "Programacion"]
        for Materia in Materias:
            query = "INSERT INTO Materia (Materia) VALUES (?)"
            self.run_query(query, (Materia,))

