from datetime import datetime
import sqlite3 as sql
  
conn = sql.connect("Registro.db")
cursor = conn.cursor()
query = cursor.execute("select * from Registro")
conn.commit()
conn.close()


##### Agregar fila "Hora" a la tabla "Registro" #####
def agg():
    cursor.execute("ALTER TABLE Registro ADD Hora text")
    conn.commit()

def Correcion():
    for i in query:
        Id = i[0]
        FechaA = i[1]

        Fechaobj = datetime.strptime(FechaA, "%Y-%m-%d %H:%M:%S.%f")
        Fecha = datetime.strftime(Fechaobj, "%Y-%m-%d")
        Hora = datetime.strftime(Fechaobj, "%H:%M:%S")

        cursor = conn.cursor()
        cursor.execute("UPDATE Registro SET Fecha = ?, Hora = ? WHERE Id = ?", (Fecha, Hora, Id))
        conn.commit()

print("""
    ------------ Menu ------------
    1. Agregar columna "Hora"
    2. Corregir columnas "Fecha" y "Hora"""
    )

resp = input("Digite una opcion: ")

if resp == "1":
    agg()
elif resp == "2":
    Correcion()





