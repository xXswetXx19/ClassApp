from tkinter import *
from tkinter import ttk, messagebox
from Clibs import Autocomplete as ac
import sqlite3 as sql

class APP:
    db_name = "database.db"
    def __init__(self, master):
        self.master = master
        self.master.title("Gestor de tareas")
        self.master.geometry("521x245")
        self.master.resizable(0,0)
        # self.master.config(bg = "#E4DFEC")
        
        self.createDB()
        self.createTable1()
        self.createTable2()
        
        
        
        query = ("SELECT Materia FROM Materias")
        Materias = self.run_query(query).fetchall()
        self.Productos = list(Materias)
        
        self.TWframe = Frame(self.master, bg = "blue")
        self.TWframe.pack(expand = True, fill = BOTH, side=LEFT)
        
        self.frame = Frame(self.master, bg = "red")
        self.frame.pack(expand=True, fill=BOTH, side=LEFT)
        
        self.entry = ac.AutocompleteCombobox(self.TWframe, width=25, font=('Times', 17),completevalues= ())
        self.entry.grid(row = 0, column = 0,sticky = W + E)
        
        self.tree = ttk.Treeview(self.TWframe, height= 10,columns = 2)
        self.tree.grid(row = 2, column = 0)
        self.tree.heading('#0', text = 'ID', anchor = CENTER)
        self.tree.column("#0",minwidth=0,width=0, stretch=NO, anchor= CENTER)
        self.tree.heading('#1', text = 'Materias', anchor = CENTER)
        self.tree.column("#1",minwidth=100,width=300, stretch=NO, anchor= CENTER)
    
        self.tree.tag_configure('datatw', font=("", 12), foreground = 'Blue')
        self.FillTw()

        self.button = Button(self.frame, text = "Crear Tarea", command = (), width=30, height=2)	
        self.button.grid(row = 0, column = 0)
        
        self.button = Button(self.frame, text = "Ver Tareas", command = (), width=30, height=2)	
        self.button.grid(row = 1, column = 0)
        
        self.button = Button(self.frame, text = "Configurar", command = (), width=30, height=2)
        self.button.grid(row = 2, column = 0)
        
        self.button = Button(self.frame, text = "Agregar Materia", command = (), width=30, height=2, anchor= CENTER)
        self.button.grid(row = 3, column = 0)
        
        
        self.button = Button(self.frame, text = "Eliminar Materia", command = (), width=30, height=2, anchor= CENTER)	
        self.button.grid(row = 4, column = 0)
        

        self.button = Button(self.frame, text = "Salir", command = self.master.destroy, width=30, height=2, anchor= CENTER)	
        self.button.grid(row = 5, column = 0, sticky = W + E)

    def FillTw(self):
        self.clearTw()
        query = 'SELECT * FROM Materias'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text = row[0], values = row[1], tags=('datatw'))
    def clearTw(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
    def createDB(self):
        conn = sql.connect(self.db_name)
        conn.commit()
        conn.close()
    def createTable1(self):
        conn = sql.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS Materias (
                Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Materia text)"""
        )
        conn.commit()
        conn.close()
    def createTable2(self):
        conn = sql.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS Cantidad (
                Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Fecha text, 
                cantidad text)""")
        conn.commit()
        conn.close()
    def run_query(self, query, parametros = ()):
        with sql.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parametros)
            conn.commit()
        return result
    def addMateria(self):
        self.Add_win = Toplevel()
        self.Add_win.resizable(width=False, height=False)
        self.Add_win.title = 'Agregar Materia'
        # self.Add_win.iconbitmap("Archivos/imgs/Icono.ico")
        def agg(Value):
            if not Value:
                return messagebox.showerror("Error", "No se puede agregar un campo vacio")
            query = f'INSERT INTO Materias VALUES(NULL, (?))'
            self.run_query(query, (Value, ))
            self.Add_win.destroy()
            self.FillTw()
        LMateria = Label(self.Add_win, text = 'Materia: ')
        LMateria.grid(row = 0, column = 0, sticky = W + E)
        CMateria = Entry(self.Add_win, width=30)
        CMateria.grid(row = 0, column = 1)
        Boton = Button(self.Add_win, text = 'Agregar', command = lambda: agg(CMateria.get()))
        Boton.grid(row = 1, column = 0, columnspan = 2, sticky = W + E)


if __name__ == '__main__':
    root = Tk()
    my_menu = APP(root)
    # my_menu.entry.focus()
    # my_menu.entry.bind('<Return>', lambda x: my_menu.validation())

    root.mainloop()
