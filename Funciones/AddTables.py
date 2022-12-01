import sqlite3 as sql

def createTable(quez):
    con = sql.connect("Registro.db")
    curso = con.cursor()
    curso.execute(quez)
    con.commit()
    con.close()
    
print("""
    ------------ Menu ------------
    1. Agregar tabla Productos
    2. Agregar tabla Presentaciones
    3. Agregar tabla Fragancias""")

resp = input("Digite una opcion: ")
if resp == "1":
    createTable(
        """CREATE TABLE IF NOT EXISTS Productos (
        Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        Producto text
    )""")
elif resp == "2":
    createTable(
        """CREATE TABLE IF NOT EXISTS Presentaciones (
        Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        Presentacion text
    )""")
elif resp == "3":
    createTable(
        """CREATE TABLE IF NOT EXISTS Fragancias (
        Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        Fragancia text
    )""")