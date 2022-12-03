from tkinter import *
from tkinter import ttk, messagebox, filedialog
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
        # Databases functions if not exist
        self.createDB()
        self.createTable1()
        self.createTable2()
        self.createTable3()

        self.Materias = self.getMaterias()
        print(self.Materias)
        
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

        # Creating Buttons and placing them with the Dic data
        ButtonsData = {
            "Crear Tarea": self.CreateTarea,
            "Ver Tareas": (),
            "Configuracion": self.configuration,
            "Agregar Materia": self.addMateria,
            "Eliminar Materia": self.removeMateria,
            "Salir": self.master.destroy
        }
        # Creating Buttons
        for i in range(len(ButtonsData.keys())):
            Button(self.frame, text = list(ButtonsData.keys())[i], command = list(ButtonsData.values())[i], width=30, height=2).grid(row = i, column = 0, sticky = W + E)
       
        # Startup Functions

        self.FillTw()
        self.getPath()

    # Global Functions
    def getPath(self):
        self.Path = self.run_query("SELECT Ruta FROM Configuracion").fetchone()
        self.Path = self.Path[0] if self.Path else ""
    def getMaterias(self):
        query = ("SELECT Materia FROM Materias")
        Materias = self.run_query(query).fetchall()
        Materias = [i[0] for i in Materias]
        return Materias
    def CreateDirs(self):
        Materias = self.getMaterias()
        for Materia in Materias:
            if self.Path:
                if not os.path.exists(f"{self.Path}\Tareas\{Materia}"):
                    os.mkdir(f"{self.Path}\Tareas\{Materia}")
            else:
                if(not os.path.exists(f'Tareas\{Materia}')):
                    os.makedirs(f'Tareas\{Materia}')
    def VerTareas(self):
        pass
    def configuration(self):
        self.Config_win = Toplevel()
        self.Config_win.resizable(width=False, height=False)
        self.Config_win.title = 'Configuración'
        self.Config_win.geometry('500x150')
        # self.Config_win.iconbitmap("Archivos/imgs/Icono.ico")
        query = 'SELECT * FROM Configuracion'
        ConfigData = self.run_query(query).fetchone()
        Values = ["Nombres:", "Apellidos:", "Paralelo:", "Ruta:"]
        
        for i in Values:
            Label(self.Config_win, text = i).place(anchor = W, relx = .1, rely = .1 + (Values.index(i) * .2))
            if ConfigData:
                Entry(self.Config_win, textvariable = StringVar(self.Config_win, value= ConfigData[Values.index(i)+1]), width=50).place(anchor = CENTER, relx = .6, rely = .1 + (Values.index(i) * .2))
            else:
                Entry(self.Config_win, width=50).place(anchor = CENTER, relx = .6, rely = .1 + (Values.index(i) * .2))
        
        Entries = [i for i in self.Config_win.children.values() if type(i) == Entry]
        RutaEntry = Entries[3]
        RutaEntry.config(state = DISABLED)
        self.getPath()
        if self.Path:
            RutaEntry['textvariable'] = StringVar(self.Config_win, value = self.Path)
        else:
            RutaEntry['textvariable'] = StringVar(self.Config_win, value = os.getcwd())
        RutaEntry.bind("<Button-1>", lambda x: browsedir())
        
        Boton1 = Button(self.Config_win, text = 'Guardar', command = lambda: agg())
        Boton1.place(anchor = CENTER, relx = .5, rely = .9)

        def agg():
            data = [i.get() for i in Entries]
            Nombres, Apellidos, Paralelo, Ruta = data
   
            if not Nombres or not Apellidos or not Paralelo:
                return messagebox.showerror("Error", "Verifique que los campos de Nombres, Apellidos y Paralelo no esten vacios")
            if ConfigData:
                query = f'UPDATE Configuracion SET Nombres = ?, Apellidos = ?, Paralelo = ?, Ruta = ? WHERE Id = ?'
                self.run_query(query, (Nombres, Apellidos, Paralelo, Ruta, ConfigData[0]))
                self.Config_win.destroy()
            else: 
                query = f'INSERT INTO Configuracion VALUES(NULL, ?, ?, ?, ?)'
                self.run_query(query, (Nombres, Apellidos, Paralelo, Ruta))
                self.Config_win.destroy()
        def browsedir():
            Dirname = filedialog.askdirectory()
            if Dirname:
                RutaEntry["textvariable"] = StringVar(self.Config_win, value = Dirname)
        
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
        Document_Path = rf'Tarea-{Fecha}-{Num}.docx'
        doc.save(Document_Path)
        os.startfile(Document_Path)
        
    def FillTw(self):
        self.clearTw()
        query = 'SELECT * FROM Materias'
        db_rows = self.run_query(query)
        for row in db_rows:
            print(row[1])
            self.tree.insert('', 0, text = row[0], values = row[1], tags=('datatw'))
    def clearTw(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
    def removeMateria(self):
        Id = self.tree.item(self.tree.selection())['text']
        if not Id:
            return messagebox.showerror("Error", "Seleccione una materia")
        query = f"DELETE FROM Materias WHERE Id = ?"
        self.run_query(query, (Id,))
        self.FillTw()

    def addMateria(self):
        self.Add_win = Toplevel()
        self.Add_win.resizable(width=False, height=False)
        self.Add_win.title = 'Agregar Materia'
        self.Add_win.geometry('300x100')
        # self.Add_win.iconbitmap("Archivos/imgs/Icono.ico")
        def agg(Value):
            if not Value:
                return messagebox.showerror("Error", "No se puede agregar un campo vacio")
            query = f'INSERT INTO Materias VALUES(NULL, (?))'
            self.run_query(query, (Value, ))
            self.Add_win.destroy()
            self.FillTw()
            self.CreateDirs()
        LMateria = Label(self.Add_win, text = 'Materia: ')
        LMateria.place(anchor = CENTER, relx = .2, rely = .3)
        CMateria = Entry(self.Add_win, width=30)
        CMateria.place(anchor = CENTER, relx = .6, rely = .3)
        Boton = Button(self.Add_win, text = 'Agregar', command = lambda: agg(CMateria.get()))
        Boton.place(anchor = CENTER, relx = .5, rely = .7)
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
                Paralelo text,
                Ruta text)""")
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
