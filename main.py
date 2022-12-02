from tkinter import *
from tkinter import ttk, messagebox
from Clibs import Autocomplete as ac
import sqlite3 as sql
from docxtpl import DocxTemplate
from datetime import datetime as date
import os

class APP:
    db_name = "database.db"
    def __init__(self, master):
        # Window config
        self.master = master
        self.master.title("Gestor de tareas")
        self.master.geometry("521x245")
        self.master.resizable(0,0)
        # self.master.config(bg = "#E4DFEC")
        self.master.bind('<KeyPress>', self.update)
        # Databases functions
        self.createDB()
        self.createTable1()
        self.createTable2()
        
        # Getting data from database
        query = ("SELECT Materia FROM Materias")
        Materias = self.run_query(query).fetchall()
        self.Materias = [i[0] for i in Materias]
        
        # Creating Frames
        self.TWframe = Frame(self.master, bg = "blue")
        self.frame = Frame(self.master, bg = "red")

        # Packing Frames
        self.TWframe.pack(expand = True, fill = BOTH, side=LEFT)
        self.frame.pack(expand=True, fill=BOTH, side=LEFT)

        # Creating Search Bar and placing it
        self.entry = ac.AutocompleteCombobox(self.TWframe, width=25, font=('Times', 17),completevalues = self.Materias)
        self.entry.grid(row = 0, column = 0,sticky = W + E)
        
        # Creating Treeview and placing it
        self.tree = ttk.Treeview(self.TWframe, height= 10,columns = 2)
        self.tree.grid(row = 2, column = 0)
        self.tree.heading('#0', text = 'ID', anchor = CENTER)
        self.tree.column("#0",minwidth=0,width=0, stretch=NO, anchor= CENTER)
        self.tree.heading('#1', text = 'Materias', anchor = CENTER)
        self.tree.column("#1",minwidth=100,width=300, stretch=NO, anchor= CENTER)
    
        # Treeview Configuration
        self.tree.tag_configure('datatw', font=("", 12), foreground = 'Black')

        # Creating Buttons
        self.button1 = Button(self.frame, text = "Crear Tarea", command = lambda: self.CreateTarea(), width=30, height=2)	      
        self.button2 = Button(self.frame, text = "Ver Tareas", command = (), width=30, height=2)	
        self.button3 = Button(self.frame, text = "Configurar", command = (), width=30, height=2)
        self.button4 = Button(self.frame, text = "Agregar Materia", command = lambda: self.addMateria(), width=30, height=2, anchor= CENTER)
        self.button5 = Button(self.frame, text = "Eliminar Materia", command = lambda: self.removeMateria(), width=30, height=2, anchor= CENTER)	
        self.button6 = Button(self.frame, text = "Salir", command = self.master.destroy, width=30, height=2, anchor= CENTER)	
        # Placing Buttons
        self.button1.grid(row = 0, column = 0)
        self.button2.grid(row = 1, column = 0)
        self.button3.grid(row = 2, column = 0)
        self.button4.grid(row = 3, column = 0)
        self.button5.grid(row = 4, column = 0)
        self.button6.grid(row = 5, column = 0)

        # Startup Functions
        self.FillTw()


    # Global Functions 
    def update(self, event):
        query = self.entry.get()
        selections = []

        if query != "":
            self.FillTw()
            for child in self.tree.get_children():
                if self.tree.item(child)['values']:
                    if query.lower() in self.tree.item(child)['values'][0].lower():
                        selections.append(child)
            for child in self.tree.get_children():
                if child not in selections:
                    self.tree.detach(child)
        else:
            self.FillTw()
        # self.tree.selection_set(selections)
    def CreateTarea(self):
        try:
            Materia = self.tree.item(self.tree.selection())['values'][0]
        except:
            return messagebox.showerror("Error", "Seleccione una materia")
        Fecha = date.strftime(date.now(), '%d.%m.%Y')
        query = f"SELECT cantidad FROM Cantidad WHERE Fecha = ?"
        Nums = self.run_query(query, (Fecha,))
        Result = list(Nums)

        if len(Result) > 0:
            Num = int(Result[0][0]) + 1
            self.run_query(f"UPDATE Cantidad SET cantidad = ? WHERE Fecha = ?", (Num, Fecha))
        else:
            self.run_query(f"INSERT INTO Cantidad VALUES (NULL, ?, ?)", (Fecha, 1))
            Num = 1
        
        doc = DocxTemplate("plantilla.docx")
        doc.render({'MATERIA': Materia, 'FECHA': Fecha.replace(".", "/")})
        # Document_Path = rf'Tareas\{Materia}\Tarea-{Fecha}-{Num}.docx'
        Document_Path = rf'\Tarea-{Fecha}-{Num}.docx'
        doc.save(Document_Path)
        os.startfile(Document_Path)
        
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
    def removeMateria(self):
        query = f"DELETE FROM Materias WHERE Id = ?"
        self.run_query(query, (self.tree.item(self.tree.selection())['text'],))
        self.FillTw()

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
    def createTable3(self):
        conn = sql.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS Configuracion (
                Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Nombres text, 
                Apellidos text,
                Paralelo)""")
        conn.commit()
        conn.close()
    def run_query(self, query, parametros = ()):
        with sql.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parametros)
            conn.commit()
        return result


if __name__ == '__main__':
    root = Tk()
    my_menu = APP(root)
    # my_menu.entry.focus()
    # my_menu.entry.bind('<Return>', lambda x: my_menu.validation())

    root.mainloop()
