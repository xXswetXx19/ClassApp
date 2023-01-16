import sqlite3 as sql


conn = sql.connect("Registro.db")
cursor = conn.cursor()
query = cursor.execute("SELECT Producto FROM Productos")
Productos = query.fetchall()
conn.commit()
conn.close()


Productos = [i[0] for i in Productos]
 
 
        
