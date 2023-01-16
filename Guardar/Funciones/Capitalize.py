import sqlite3 as sql
import time
inicio = time.time()
  
conn = sql.connect("Registro.db")
cursor = conn.cursor()
query = cursor.execute("select Producto from Registro")
conn.commit()

#### Capitalize all the values of the column Producto ####
for i in query:
    formated = i[0].strip().capitalize()
    cursor = conn.cursor()
    cursor.execute("UPDATE Registro SET Producto = ? WHERE Producto = ?", (str(formated), str(i[0])))
    print(f"{str(i[0])} -> {str(formated)}")
    conn.commit()
fin = time.time()
print(f"Realizado en {fin - inicio} segundos")

