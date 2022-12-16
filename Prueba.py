from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkinter.ttk import Combobox
from Clibs import Autocomplete as ac
import sqlite3 as sql
from docxtpl import DocxTemplate
from datetime import datetime as date
import os
import subprocess

# Global Variables
db_name = "database.db"

def createDB():
    conn = sql.connect(db_name)
    conn.commit()
    conn.close()
def createTable1():
    conn = sql.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Materias (
            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Materia text)"""
    )
    conn.commit()
    conn.close()
def createTable2():
    conn = sql.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Cantidad (
            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Fecha text, 
            cantidad text)""")
    conn.commit()
    conn.close()
def createTable3():
    conn = sql.connect(db_name)
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
def run_query(query, parametros = ()):
    with sql.connect(db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parametros)
        conn.commit()
    return result
def getPath():
    global Path
    Path = run_query("SELECT Ruta FROM Configuracion").fetchone()
    Path = Path[0] if Path else os.getcwd()
    return Path
def getMaterias():
    query = ("SELECT Materia FROM Materias")
    Materias = run_query(query).fetchall()
    Materias = [i[0] for i in Materias]
    return Materias

# Startup Functions
createDB()
createTable1()
createTable2()
createTable3()

class Tarea:
    def __init__(self, Materia, Fecha, Descripcion, Prioridad):
        self.Materia = Materia     
        self.Descripcion = Descripcion
        self.Prioridad = Prioridad
        self.Fecha = Fecha
    def __str__(self) -> str:
        return f"{self.Materia} + {self.Fecha} + {self.Prioridad}"
class TareaGrupal(Tarea):
    def __init__(self, Materia, Fecha, Descripcion, Integrantes):
        super().__init__(Materia = Materia, Fecha = Fecha, Descripcion = Descripcion)
        self.Integrantes = Integrantes

# Clasess

class APP:
    def __init__(self, master):
        # Window config
        self.master = master
        self.master.title("Gestor de tareas")
        self.master.geometry("521x248")
        self.master.resizable(0,0)
        self.master.iconbitmap("Icono.ico")
        # Event binds
        self.master.bind('<KeyPress>', self.__update)
        self.master.bind("<FocusIn>", self.__update)
        # Creating Frames
        self.TWframe = Frame(self.master)
        self.frame = Frame(self.master)
        # Packing Frames
        self.TWframe.pack(expand = True, fill = BOTH, side=LEFT)
        self.frame.pack(expand=True, fill=BOTH, side=LEFT)
        # Creating Search Bar and placing it
        self.entry = ac.AutocompleteCombobox(self.TWframe, width=25,completevalues = lambda: getMaterias)
        self.entry.grid(row = 0, column = 0,sticky = W + E)
        # Creating Treeview and placing it
        self.tree = ttk.Treeview(self.TWframe, height= 10,columns = 2)
        self.tree.grid(row = 2, column = 0)
        self.tree.heading('#0', text = 'ID', anchor = CENTER)
        self.tree.column("#0",minwidth=0,width=0, stretch=NO, anchor= CENTER)
        self.tree.heading('#1', text = 'Materias', anchor = CENTER)
        self.tree.column("#1",minwidth=100,width=300, anchor= CENTER)
        # Treeview Configuration
        self.tree.tag_configure('Materias', font=("", 10), foreground = 'Black')
        # Creating Buttons and placing them with the Dic data
        ButtonsData = {
            "Crear Tarea": self.CreateTarea,
            "Ver Tareas": self.VerTareas,
            "Calendario": (),
            "Agendar Tarea": (),
            "Configuracion": self.configuration,
            "Agregar Materia": self.addMateria,
            "Eliminar Materia": self.removeMateria,
            "Salir": self.master.destroy
        }
        # Creating Buttons
        for i in range(len(ButtonsData.keys())):
            Button(self.frame, text = list(ButtonsData.keys())[i], command = list(ButtonsData.values())[i], width=30).pack(fill=BOTH, expand=True)
        # Startup Functions
        self.FillTw()
        getPath()
        self.__updateList()
    def __updateList(self):
        self.Materias = getMaterias()
        self.entry['completevalues'] = self.Materias
    def CreateDirs(self):
        Materias = getMaterias()
        if not os.path.exists(f"{Path}\Tareas"):
            os.mkdir(f"{Path}\Tareas")
        for Materia in Materias:
            if not os.path.exists(f"{Path}\Tareas\{Materia}"):
                os.mkdir(f"{Path}\Tareas\{Materia}") 
    def __update(self, event):
        query = self.entry.get()
        selections = []
        if event.keysym == "BackSpace":
            if self.entry.selection_present():
                query = query.replace(query.selection_get(), "")
        else:
            query = query[:-1]
        if event.char.isalnum() and query == "":
            query += event.char
        if query != "":
            self.FillTw()
            for child in self.tree.get_children():
                if self.tree.item(child)['values']:
                    if str(query.lower()) in self.tree.item(child)['values'][0].lower():
                        selections.append(child)
            for child in self.tree.get_children():
                if child not in selections:
                    self.tree.detach(child)
        else:
            self.FillTw()
        if len(selections) == 1:
            self.tree.selection_set(selections)
    def CreateTarea(self):
        try:
            Materia = self.tree.item(self.tree.selection())['values'][0]
        except:
            return messagebox.showerror("Error", "Seleccione una materia")
        DatosConfig = run_query("SELECT * FROM Configuracion").fetchone()
        if not DatosConfig:
            return messagebox.showerror("Error", "Agregue sus datos en la configuracion para crear una tarea")
        Id, Nombres, Apellidos, Paralelo, Ruta = DatosConfig   
        if not os.path.exists(f"{Path}\Tareas\{Materia}"):
            self.CreateDirs()
        Fecha = date.strftime(date.now(), '%d.%m.%Y')
        Nums = run_query(f"SELECT cantidad FROM Cantidad WHERE Fecha = ?", (Fecha,))
        Result = list(Nums)
        if len(Result) > 0:
            Num = int(Result[0][0]) + 1
            run_query(f"UPDATE Cantidad SET cantidad = ? WHERE Fecha = ?", (Num, Fecha))
        else:
            run_query(f"INSERT INTO Cantidad VALUES (NULL, ?, ?)", (Fecha, 1))
            Num = 1
        doc = DocxTemplate("plantilla.docx")
        doc.render({ 'MATERIA': Materia, 'FECHA': Fecha.replace(".", "/"), 'NOMBRES': Nombres, 'APELLIDOS': Apellidos, 'PARALELO': Paralelo })
        Document_Path = rf'{Path}/Tareas/{Materia}/Tarea-{Fecha}-{Num}.docx'
        doc.save(Document_Path)
        os.startfile(Document_Path)
        try:
            self.view_win_functions.getHomeworks()
        except:
            pass

    def FillTw(self):
        self.clearTw()
        db_rows = run_query('SELECT * FROM Materias')
        for row in db_rows:
            Materia = (row[1],)
            self.tree.insert('', 0, text = row[0], values = Materia, tags=('Materias'))
    def clearTw(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
    def removeMateria(self):
        Id = self.tree.item(self.tree.selection())['text']
        if not Id:
            return messagebox.showerror("Error", "Seleccione una materia")
        run_query(f"DELETE FROM Materias WHERE Id = ?", (Id,))
        self.FillTw()
    def addMateria(self):
        if any(isinstance(x, Toplevel) for x in self.master.winfo_children()):
            if self.Add_win.winfo_exists() if self.Add_win.winfo_exists() else False:
                messagebox.showerror("Error", "Ya hay una ventana")
                return self.Add_win.lift() 
        self.Add_win = Toplevel()
        self.Add_win.resizable(width=False, height=False)
        self.Add_win.title = 'Agregar Materia'
        self.Add_win.geometry('300x100')
        self.Add_win.iconbitmap("Icono.ico")
        def agg(Value):
            Value = Value.strip().capitalize()
            if not Value:
                return messagebox.showerror("Error", "No se puede agregar un campo vacio")
            if not Value.replace(" ","").isalnum(): # Revisa que value solo tenga numeros y letras, nada de simbolos
                return messagebox.showerror("Error", "El nombre de la materia solo puede contener letras y numeros")
            if run_query(f"SELECT * FROM Materias WHERE Materia = ?", (Value,)).fetchone():
                return messagebox.showerror("Error", "La materia ya existe")
            run_query(f'INSERT INTO Materias VALUES(NULL, (?))', (Value, ))
            self.Add_win.destroy()
            self.FillTw()
            self.CreateDirs()
            self.__updateList()
        LMateria = Label(self.Add_win, text = 'Materia: ').place(anchor = CENTER, relx = .2, rely = .3)
        CMateria = Entry(self.Add_win, width=30)
        CMateria.place(anchor = CENTER, relx = .6, rely = .3)
        Boton = Button(self.Add_win, text = 'Agregar', command = lambda: agg(CMateria.get())).place(anchor = CENTER, relx = .5, rely = .7)
        self.Add_win.bind('<Return>', lambda event: agg(CMateria.get()))
    def VerTareas(self):
        if any(isinstance(x, Toplevel) for x in self.master.winfo_children()):
            if self.view_wins.winfo_exists() if self.view_wins.winfo_exists() else False:
                messagebox.showerror("Error", "Ya hay un visualizador de tareas abierto")
                return self.view_wins.lift() 
        self.view_wins = Toplevel(self.master)
        self.view_win_functions = WinHomeworks(self.view_wins)
    def configuration(self):
        if any(isinstance(x, Toplevel) for x in self.master.winfo_children()):
            if (self.config_win.winfo_exists() if self.config_win.winfo_exists() else False):
                messagebox.showerror("Error", "Ya hay una ventana de configuracion abierta")
                return self.config_win.lift() 
        self.config_win = Toplevel(self.master)
        ConfigWin(self.config_win)

class ConfigWin:
    def __init__(self, toplevel):
        self.Config_win = toplevel
        self.Config_win.resizable(width=False, height=False)
        self.Config_win.title = 'Configuración'
        self.Config_win.geometry('500x150')
        self.Config_win.iconbitmap("Icono.ico")
         
        self.ConfigData = run_query('SELECT * FROM Configuracion').fetchone()
        Datos = ["Nombres:", "Apellidos:", "Paralelo:", "Ruta:"]
        
        for i in Datos:
            Label(self.Config_win, text = i).place(anchor = W, relx = .1, rely = .1 + (Datos.index(i) * .2))
            if self.ConfigData:
                Entry(self.Config_win, textvariable = StringVar(self.Config_win, value= self.ConfigData[Datos.index(i)+1]), width=50).place(anchor = CENTER, relx = .6, rely = .1 + (Datos.index(i) * .2))
            else:
                Entry(self.Config_win, width=50).place(anchor = CENTER, relx = .6, rely = .1 + (Datos.index(i) * .2))
        
        self.Entries = [i for i in self.Config_win.children.values() if type(i) == Entry]
        self.RutaEntry = self.Entries[3]
        self.RutaEntry.config(state = DISABLED)
        getPath()
        self.RutaEntry['textvariable'] = StringVar(self.Config_win, value = Path)
        self.RutaEntry.bind("<Button-1>", lambda x: self.browsedir())
        
        Boton1 = Button(self.Config_win, text = 'Guardar', command = lambda: self.agg())
        Boton1.place(anchor = CENTER, relx = .5, rely = .9)
        self.Config_win.bind('<Return>', lambda event: self.agg())
    def agg(self):
        data = [i.get() for i in self.Entries]
        Nombres, Apellidos, Paralelo, Ruta = data
        if not Nombres or not Apellidos or not Paralelo:
            return messagebox.showerror("Error", "Verifique que los campos de Nombres, Apellidos y Paralelo no esten vacios")
        if self.ConfigData:
            Id = self.ConfigData[0]
            query = f'UPDATE Configuracion SET Nombres = ?, Apellidos = ?, Paralelo = ?, Ruta = ? WHERE Id = ?'
            run_query(query, (Nombres.strip(), Apellidos.strip(), Paralelo.strip(), Ruta, Id))
            self.Config_win.destroy()
        else: 
            query = f'INSERT INTO Configuracion VALUES(NULL, ?, ?, ?, ?)'
            run_query(query, (Nombres, Apellidos, Paralelo, Ruta))
            self.Config_win.destroy()
        getPath()
    def browsedir(self):
        Dirname = filedialog.askdirectory()
        if Dirname:
            self.RutaEntry["textvariable"] = StringVar(self.Config_win, value = Dirname)  

class WinHomeworks:
    def __init__(self, toplevel):
        self.view_wins = toplevel
        self.view_wins.title("Tareas")
        self.view_wins.geometry("650x275")
        self.view_wins.resizable(0,0)
        self.view_wins.config(bg = "")
        self.view_wins.iconbitmap("Icono.ico")
        self.Materias = getMaterias()
        
        self.view_frame = Frame(self.view_wins, bg = "#E4DFEC")
        self.view_frame.pack(expand = True, fill = BOTH)

        self.view_topframes = Frame(self.view_frame, bg = "#E4DFEC")
        self.view_topframes.grid(row = 0, column = 0, sticky = W + E)

        self.view_ClasesEntry = Combobox(self.view_topframes, width=10, font=('', 12), values = self.Materias)
        self.view_ClasesEntry.grid(row = 0, column = 0,sticky = W + E)

        self.view_topframes.columnconfigure(0, minsize=200)
        self.view_topframes.columnconfigure(1, minsize=150)
        self.view_topframes.columnconfigure(2, minsize=150)
        self.view_topframes.columnconfigure(3, minsize=150)
        for i in range(3):
            Entry(self.view_topframes, width=10, font=('', 12)).grid(row = 0, column = i + 1,sticky = W + E)
        # Getting the entries from a frame and giving events to them
        self.entries = [i for i in self.view_topframes.children.values() if type(i) == Entry or type(i) == Combobox]
        for index, entrie in enumerate(self.entries):
            entrie.bind("<KeyPress>", lambda event, entry = entrie, index = index: self.filterupdate(event, entry, index))
            entrie.bind("<FocusIn>", lambda event, entry = entrie, index = index: self.filterupdate(event, entry, index))
        
        # Creating Treeview
        self.view_tree = ttk.Treeview(self.view_frame, height= 10,columns = ("#1", "#2", "#3", "#4"))
        self.view_tree.grid(row = 1, column = 0)
        self.view_tree.heading('#0', text = 'ID', anchor = CENTER)
        self.view_tree.column("#0",minwidth=0,width=0, stretch=NO, anchor= CENTER)
        self.view_tree.heading("#1", text = 'Materia', anchor = CENTER)
        self.view_tree.column("#1",minwidth=100,width=200, anchor= W)
        self.view_tree.heading("#2", text = 'Num', anchor = CENTER)
        self.view_tree.column("#2",minwidth=100,width=150, anchor= CENTER)
        self.view_tree.heading("#3", text = 'Fecha', anchor = CENTER)
        self.view_tree.column("#3",minwidth=100,width=150, anchor= CENTER)
        self.view_tree.heading("#4", text = 'Hora', anchor = CENTER)
        self.view_tree.column("#4",minwidth=100,width=150, anchor= CENTER)

        self.view_buttons_frame = Frame(self.view_frame, bg = "BLUE")
        self.view_buttons_frame.grid(row= 2, column = 0, columnspan=3)
        
        self.view_buttons_frame.columnconfigure(0, minsize=216)
        self.view_buttons_frame.columnconfigure(1, minsize=216)
        self.view_buttons_frame.columnconfigure(2, minsize=216)

        ButtonsData = { "Eliminar": self.DeleteHomework, "Ubicacion": self.OpenPath, "Abrir": self.OpenHomework }
        for i in range(len(ButtonsData.keys())):
            Button(self.view_buttons_frame, text = list(ButtonsData.keys())[i], command= list(ButtonsData.values())[i], width=10, height=1).grid(row = 0, column = i, sticky = W + E)

        self.view_tree.tag_configure('Tareas', font=("", 10), foreground = 'Black')
        # Startup functions
        getPath()
        self.getHomeworks()  
    def clearviewTw(self):
        records = self.view_tree.get_children()
        for element in records:
            self.view_tree.delete(element)

    def filterupdate(self, event, entry, index):
        selections = []
        query = entry.get()
        if event.keysym == "BackSpace":
            if entry.selection_present():
                query = query.replace(entry.selection_get(), "")
            else:
                query = query[:-1]
        if event.char.isalnum() and len(query) == 0:
            query += event.char
        if query != "":
            self.getHomeworks()
            for child in self.view_tree.get_children():
                if self.view_tree.item(child)['values']:
                    if query.lower() in str(self.view_tree.item(child)['values'][index]).lower():
                        selections.append(child)
            for child in self.view_tree.get_children():
                if child not in selections:
                    self.view_tree.detach(child)
        else:
            self.getHomeworks()
    def getHomeworks(self):
        self.clearviewTw()
        if os.path.exists(f"{Path}\Tareas"):
            Classdirs = os.listdir(f"{Path}\Tareas")
            for ClassDir in Classdirs:
                if os.path.isdir(f"{Path}\Tareas\{ClassDir}"):
                    Homeworks = os.scandir(f"{Path}\Tareas\{ClassDir}")
                    for Homework in Homeworks:
                        timestamp = os.path.getctime(Homework.path)
                        Date = date.fromtimestamp(timestamp).strftime('%d/%m/%Y')
                        Hour = date.fromtimestamp(timestamp).strftime('%H:%M')
                        Num = Homework.name.split("-")[2].split(".")[0]
                        self.view_tree.insert('', 0, text = Homework, values = (ClassDir, Num, Date, Hour), tags = ("Tareas"))
    def DeleteHomework(self):
        try:
            Homework = self.view_tree.item(self.view_tree.selection())['text'].split("'")[1]
            Class = self.view_tree.item(self.view_tree.selection())['values'][0]
        except:
            return messagebox.showerror("Error", "No se ha seleccionado ninguna tarea")
        ask = messagebox.askyesno("¿Esta seguro de eliminar la tarea?", "¿Esta seguro de eliminar la tarea?")
        if ask:
            os.remove(f"{Path}\Tareas\{Class}\{Homework}")
            self.view_tree.delete(self.view_tree.selection())
        else:      return
    def OpenHomework(self):
        try:
            Homework = self.view_tree.item(self.view_tree.selection())['text'].split("'")[1]
            Class = self.view_tree.item(self.view_tree.selection())['values'][0]
        except:
            return messagebox.showerror("Error", "No se ha seleccionado ninguna tarea")
        os.startfile(f"{Path}\Tareas\{Class}\{Homework}")
    def OpenPath(self):
        try:
            Homework = self.view_tree.item(self.view_tree.selection())['text'].split("'")[1]
            Class = self.view_tree.item(self.view_tree.selection())['values'][0]
        except:
            return messagebox.showerror("Error", "No se ha seleccionado ninguna tarea")
        HomeWorkPath = f"{Path}\\Tareas\\{Class}\\{Homework}".replace("/", "\\") 
        subprocess.Popen(r'explorer /select,"{FilePath}"'.format(FilePath=HomeWorkPath))

class Calendario:
    def __init__(self, toplevel):
        self.Calendario_win = toplevel
        self.Calendario_win.title("Tareas")
        self.Calendario_win.geometry("650x275")
        self.Calendario_win.resizable(0,0)
        self.Calendario_win.config(bg = "")
        self.Calendario_win.iconbitmap("Icono.ico")
        self.Materias = getMaterias()
        
        
if __name__ == '__main__':
    root = Tk()
    my_menu = APP(root)
    root.mainloop()