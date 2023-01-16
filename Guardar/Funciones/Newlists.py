import sqlite3 as sql
import pandas as pd

def agg(Archivo, Tabla):
    conn = sql.connect("Registro.db")
    cursor = conn.cursor()
    
    read = pd.read_excel(Archivo)
    Productos = pd.unique(read.values.ravel('K'))

    for value in Productos:
        print(f"Insertando: {value}" )
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO {Tabla} VALUES(NULL, ?)', (value, ))
        conn.commit()
    conn.close()


agg("Fragancias.xlsx", "Fragancias")
