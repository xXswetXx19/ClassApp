import sqlite3 as sql
import os
import pandas as pd
  
conn = sql.connect("Registro.db")
cursor = conn.cursor()
query = cursor.execute("select Fragancia from Registro")
conn.commit()
productos = sorted(list(set(query)))


def dbtoexcel():
    desktopath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')   
    df = pd.DataFrame(productos, columns=['Fragancia'])
    df.to_excel("Fragancias.xlsx", index=False)
    os.startfile('Fragancias.xlsx')

def exceltodb():
    read = pd.read_excel("Fragancias.xlsx")
    read = pd.DataFrame(read).values.tolist()

    for i in read:
        print(f"{i[0]} -> {i[1]}" )
        Antigua = i[0]
        Correcion = i[1]
        cursor = conn.cursor()
        cursor.execute("UPDATE Registro SET Fragancia = ? WHERE Fragancia = ?", (str(Correcion), str(Antigua)))
        conn.commit()

print("""
--------------- Menu ---------------
1. Exportar de base de datos a Excel
2. Importar de Excel a base de datos
------------------------------------""")

opcion = int(input("Seleccione una opcion: "))
if opcion == 1:
    dbtoexcel()
elif opcion == 2:
    exceltodb()

