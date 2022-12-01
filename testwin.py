from tkinter import *
from tkinter import ttk, messagebox
from Clibs import Autocomplete as ac
import sqlite3 as sql



# Variables

class Menu:
    def __init__(self, master):
        self.db_name = "database.db"

        query = ("SELECT Materia FROM Materias")
        Materias = self.run_query(query).fetchall()
        self.Productos = list(Materias)


        self.master = master
        self.frame = Frame(self.master, bg = "#E4DFEC")
        self.frame.pack()

        self.button = Button(self.frame, text = "Agregar", command = self.agregar)
        self.button.pack()
        self.button = Button(self.frame, text = "Salir", command = self.master.destroy)	
        self.button.pack()

        self.entry = ac.AutocompleteCombobox(self.frame, width=20, font=('Times', 18),completevalues= self.Productos)
        self.entry.pack()
        
        def createDB():
            conn = sql.connect(self.db_name)
            conn.commit()
            conn.close()
            
        def createTable1():
            conn = sql.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
              f"""CREATE TABLE IF NOT EXISTS Materias (
                  Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                  Materia text, 
            )"""
            )
            conn.commit()
            conn.close()
        def createTable2():
            conn = sql.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
              f"""CREATE TABLE IF NOT EXISTS Cantidad (
                  Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                  Fecha text, 
                  cantidad text, 
            )"""
            )
            conn.commit()
            conn.close()
        
        createDB()
        createTable1()
        createTable2()

    def run_query(self, query, parametros = ()):
        with sql.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parametros)
            conn.commit()
        return result

    def agregar(self):
        self.Add_win = Toplevel()
        self.Add_win.resizable(width=False, height=False)
        self.Add_win.title = 'Agregar'
        # self.Add_win.iconbitmap("Archivos/imgs/Icono.ico")
        Categorias = ['Productos', 'Presentaciones', 'Fragancias']

        #Nombre Nuevo
        Label(self.Add_win, text = 'Categoria: ').grid(row = 1, column = 1)
        CCategoria = ac.AutocompleteCombobox(self.Add_win, completevalues = Categorias, width=15)
        CCategoria.grid(row = 1, column = 2)

        Label(self.Add_win, text = 'Producto: ').grid(row = 2, column = 1)
        CValue = Entry(self.Add_win, width=18)
        CValue.grid(row = 2, column = 2)

        def agg(Categoria, Value):
            if not Categoria or not Value:
                messagebox.showwarning('Advertencia', 'Por favor llena todos los campos.')
                return
            print(Categoria, Value)
            query = f'INSERT INTO {Categoria} VALUES(NULL, (?))'
            self.run_query(query, (Value, ))
            self.entry["completevalues"] = self.Productos
            self.Add_win.destroy()
        
        Boton = Button(self.Add_win, text = 'Agregar', command = lambda: agg(CCategoria.get(), CValue.get()))
        Boton.grid(row = 3, column = 2)


if __name__ == '__main__':
    root = Tk()
    root.title("Registro de ventas")
    root.geometry("300x100")
    root.resizable(0,0)
    root.config(bg = "#E4DFEC")

    my_menu = Menu(root)
    my_menu.entry.focus()
    # my_menu.entry.bind('<Return>', lambda x: my_menu.validation())

    root.mainloop()
