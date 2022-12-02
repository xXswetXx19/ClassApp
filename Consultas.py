import sqlite3 as sql

def consulta(Tabla):
    conn = sql.connect("database.db")
    cursor = conn.cursor()
    respuesta = cursor.execute("SELECT * FROM {}".format(Tabla))
    respuesta = list(respuesta)
    conn.commit()
    conn.close()
    return respuesta

def consultanz(query):
    conn = sql.connect("database.db")
    cursor = conn.cursor()
    respuesta = cursor.execute(query)
    respuesta = list(respuesta)
    conn.commit()
    conn.close()
    return respuesta

menu = """"
Que deseas hacer?
1) Realizar una consulta
2) Consulta avanzada"""
print(menu)
resp = input("Escribe el numero de la opcion que deseas: ")

if resp == "1":
    resp = input("Digita el nombre de la tabla: ")
    print(consulta(resp))
if(resp == "2"):
    resp = input("Digita la consulta: ")
    print(consultanz(resp))