from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkinter.ttk import Combobox
from Clibs import Autocomplete as ac
import sqlite3 as sql
from docxtpl import DocxTemplate
from datetime import datetime as date
import os

# Global Variables
db_name = "database.db"
# Global fuctions
def run_query(query, parametros = ()):
    with sql.connect(db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parametros)
        conn.commit()
    return result
def getPath():
    Path = run_query("SELECT Ruta FROM Configuracion").fetchone()
    Path = Path[0] if Path else os.getcwd()
    return Path
def getMaterias():
    query = ("SELECT Materia FROM Materias")
    Materias = run_query(query).fetchall()
    Materias = [i[0] for i in Materias]
    return Materias

# Clasess
class APP:
    def __init__(self, master):
        # Window config
        self.master = master
        self.master.title("Gestor de tareas")
        self.master.geometry("521x245")
        self.master.resizable(0,0)
        # self.master.config(bg = "#E4DFEC")
        self.master.bind('<KeyPress>', self.update)
        self.master.bind("<FocusIn>", self.update)
        # Databases functions if not exist
        self.createDB()
        self.createTable1()
        self.createTable2()
        self.createTable3()
        # Creating Frames
        self.TWframe = Frame(self.master)
        self.frame = Frame(self.master)
        # Packing Frames
        self.TWframe.pack(expand = True, fill = BOTH, side=LEFT)
        self.frame.pack(expand=True, fill=BOTH, side=LEFT)
        # Creating Search Bar and placing it
        self.entry = ac.AutocompleteCombobox(self.TWframe, width=25, font=('Times', 17),completevalues = ())
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
        self.Path = getPath()
        self.updateList()
    # Global Functions
    def updateList(self):
        self.Materias = getMaterias()
        self.entry['completevalues'] = self.Materias
    def CreateDirs(self):
        Materias = getMaterias()
        if not os.path.exists(f"{self.Path}\Tareas"):
            os.mkdir(f"{self.Path}\Tareas")
        for Materia in Materias:
            if not os.path.exists(f"{self.Path}\Tareas\{Materia}"):
                os.mkdir(f"{self.Path}\Tareas\{Materia}")
    # MAIN FUCTIONS     
    def update(self, event):
        query = self.entry.get()
        selections = []
        if event.keysym == "BackSpace":
            if self.entry.selection_present():
                query = query.replace(query.selection_get(), "")
        else:
            query = query[:-1]
        if event.char.isalpha() and query == "":
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
        if DatosConfig:
            Id, Nombres, Apellidos, Paralelo, Ruta = DatosConfig
        else:
            return messagebox.showerror("Error", "Agregue sus datos en la configuracion para crear una tarea")
        if not os.path.exists(f"{self.Path}\Tareas\{Materia}"):
            self.CreateDirs()
        Fecha = date.strftime(date.now(), '%d.%m.%Y')
        Hora = date.strftime(date.now(), '%H.%M.%S')
        query = f"SELECT cantidad FROM Cantidad WHERE Fecha = ?"
        Nums = run_query(query, (Fecha,))
        Result = list(Nums)

        if len(Result) > 0:
            Num = int(Result[0][0]) + 1
            run_query(f"UPDATE Cantidad SET cantidad = ? WHERE Fecha = ?", (Num, Fecha))
        else:
            run_query(f"INSERT INTO Cantidad VALUES (NULL, ?, ?)", (Fecha, 1))
            Num = 1
        doc = DocxTemplate("plantilla.docx")
        doc.render(
        {'MATERIA': Materia, 
         'FECHA': Fecha.replace(".", "/"),
         'NOMBRES': Nombres,
         'APELLIDOS': Apellidos,
         'PARALELO': Paralelo,
         })
        Document_Name_Format = f"Tarea-{Fecha}-{Num}.docx"
        Document_Path = rf'{self.Path}/Tareas/{Materia}/{Document_Name_Format}'
        doc.save(Document_Path)
        # open the file
        os.startfile(Document_Path)
        # updating the view_treeviewer if the view_win is open
        try:
            self.view_win_functions.getHomeworks() 
        except:
            pass
    def FillTw(self):
        self.clearTw()
        query = 'SELECT * FROM Materias'
        db_rows = run_query(query)
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
        query = f"DELETE FROM Materias WHERE Id = ?"
        run_query(query, (Id,))
        self.FillTw()

    def addMateria(self):
        self.Add_win = Toplevel()
        self.Add_win.resizable(width=False, height=False)
        self.Add_win.title = 'Agregar Materia'
        self.Add_win.geometry('300x100')
        # self.Add_win.iconbitmap("Archivos/imgs/Icono.ico")
        def agg(Value):
            Value = Value.strip().capitalize()
            if not Value:
                return messagebox.showerror("Error", "No se puede agregar un campo vacio")
            
            if not Value.replace(" ","").isalnum():
                return messagebox.showerror("Error", "El nombre de la materia solo puede contener letras y numeros")
            if run_query(f"SELECT * FROM Materias WHERE Materia = ?", (Value,)).fetchone():
                return messagebox.showerror("Error", "La materia ya existe")
            query = f'INSERT INTO Materias VALUES(NULL, (?))'
            run_query(query, (Value, ))
            self.Add_win.destroy()
            self.FillTw()
            self.CreateDirs()
            self.updateList()
        LMateria = Label(self.Add_win, text = 'Materia: ')
        LMateria.place(anchor = CENTER, relx = .2, rely = .3)
        CMateria = Entry(self.Add_win, width=30)
        CMateria.place(anchor = CENTER, relx = .6, rely = .3)
        Boton = Button(self.Add_win, text = 'Agregar', command = lambda: agg(CMateria.get()))
        Boton.place(anchor = CENTER, relx = .5, rely = .7)
        self.Add_win.bind('<Return>', lambda event: agg(CMateria.get()))
    def createDB(self):
        conn = sql.connect(db_name)
        conn.commit()
        conn.close()
    def createTable1(self):
        conn = sql.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS Materias (
                Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Materia text)"""
        )
        conn.commit()
        conn.close()
    def createTable2(self):
        conn = sql.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS Cantidad (
                Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Fecha text, 
                cantidad text)""")
        conn.commit()
        conn.close()
    def createTable3(self):
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
    def VerTareas(self):
        self.view_wins = Toplevel(self.master)
        self.view_win_functions = WinHomeworks(self.view_wins)
        self.view_wins.title("Tareas")
        self.view_wins.geometry("650x275")
        self.view_wins.resizable(0,0)
        self.view_wins.config(bg = "")
    def configuration(self):
        self.config_win = Toplevel(self.master)
        self.config_win_functions = ConfigWin(self.config_win)
        self.config_win.resizable(width=False, height=False)
        self.config_win.title = 'Configuración'
        self.config_win.geometry('500x150')
        # self.Config_win.iconbitmap("Archivos/imgs/Icono.ico")
class ConfigWin:
    def __init__(self, toplevel):
        self.Config_win = toplevel
        query = 'SELECT * FROM Configuracion'
        self.ConfigData = run_query(query).fetchone()
        Values = ["Nombres:", "Apellidos:", "Paralelo:", "Ruta:"]
        
        for i in Values:
            Label(self.Config_win, text = i).place(anchor = W, relx = .1, rely = .1 + (Values.index(i) * .2))
            if self.ConfigData:
                Entry(self.Config_win, textvariable = StringVar(self.Config_win, value= self.ConfigData[Values.index(i)+1]), width=50).place(anchor = CENTER, relx = .6, rely = .1 + (Values.index(i) * .2))
            else:
                Entry(self.Config_win, width=50).place(anchor = CENTER, relx = .6, rely = .1 + (Values.index(i) * .2))
        
        self.Entries = [i for i in self.Config_win.children.values() if type(i) == Entry]
        self.RutaEntry = self.Entries[3]
        self.RutaEntry.config(state = DISABLED)
        self.Path = getPath()
        self.RutaEntry['textvariable'] = StringVar(self.Config_win, value = self.Path)
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
            query = f'UPDATE Configuracion SET Nombres = ?, Apellidos = ?, Paralelo = ?, Ruta = ? WHERE Id = ?'
            run_query(query, (Nombres.strip(), Apellidos.strip(), Paralelo.strip(), Ruta, self.ConfigData[0]))
            self.Config_win.destroy()
        else: 
            query = f'INSERT INTO Configuracion VALUES(NULL, ?, ?, ?, ?)'
            run_query(query, (Nombres, Apellidos, Paralelo, Ruta))
            self.Config_win.destroy()
    def browsedir(self):
        Dirname = filedialog.askdirectory()
        if Dirname:
            self.RutaEntry["textvariable"] = StringVar(self.Config_win, value = Dirname)  

class WinHomeworks:
    db_name = 'database.db'
    def __init__(self, toplevel):
        self.view_wins = toplevel

        self.Materias = getMaterias()
        self.Path = getPath()
        self.view_frame = Frame(self.view_wins, bg = "#E4DFEC")
        self.view_frame.pack(expand = True, fill = BOTH)

        self.view_topframes = Frame(self.view_frame, bg = "#E4DFEC")
        self.view_topframes.grid(row = 0, column = 0, sticky = W + E)

        self.view_ClasesEntry = Combobox(self.view_topframes, width=10, font=('', 12), values = self.Materias)
        self.view_ClasesEntry.grid(row = 0, column = 0,sticky = W + E)

        self.view_NumEntry = Entry(self.view_topframes, width=10, font=('', 12))
        self.view_NumEntry.grid(row = 0, column = 1,sticky = W + E)
        self.view_DateEntry = Entry(self.view_topframes, width=10, font=('', 12))
        self.view_DateEntry.grid(row = 0, column = 2,sticky = W + E)
        self.view_HourEntry = Entry(self.view_topframes, width=10, font=('', 12))
        self.view_HourEntry.grid(row = 0, column = 3,sticky = W + E)

        self.view_topframes.columnconfigure(0, minsize=200)
        self.view_topframes.columnconfigure(1, minsize=150)
        self.view_topframes.columnconfigure(2, minsize=150)
        self.view_topframes.columnconfigure(3, minsize=150)

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
        self.view_buttons_frame.grid(row= 2, column = 0, columnspan=2)

        self.view_buttons_frame.columnconfigure(0, minsize=325)
        self.view_buttons_frame.columnconfigure(1, minsize=325)

        self.view_button = Button(self.view_buttons_frame, text = "Abrir", command = self.OpenHomework, width=10, height=1)
        self.view_button.grid(row = 0, column = 0, sticky = W + E)
        self.view_button2 = Button(self.view_buttons_frame, text = "Eliminar", command = self.DeleteHomework, width=10, height=1)
        self.view_button2.grid(row = 0, column = 1, sticky = W + E)
        self.view_tree.tag_configure('Tareas', font=("", 10), foreground = 'Black')
        # Startup functions
        self.getHomeworks()  
    def clearviewTw(self):
        records = self.view_tree.get_children()
        for element in records:
            self.view_tree.delete(element)

    def filterupdate(self, event, entry, index):
        if index == 2: 
            self.dateformat(event)
        selections = []
        query = entry.get()
        if event.keysym == "BackSpace":
            if entry.selection_present():
                query = query.replace(entry.selection_get(), "")
            else:
                query = query[:-1]
        if event.char.isdigit() or event.char.isalpha() and len(query) > 0:
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
        if os.path.exists(f"{self.Path}\Tareas"):
            Classdirs = os.listdir(f"{self.Path}\Tareas")
            for ClassDir in Classdirs:
                if os.path.isdir(f"{self.Path}\Tareas\{ClassDir}"):
                    Homeworks = os.scandir(f"{self.Path}\Tareas\{ClassDir}")
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
            os.remove(f"{self.Path}\Tareas\{Class}\{Homework}")
            self.view_tree.delete(self.view_tree.selection())
        else:      return
    def OpenHomework(self):
        try:
            Homework = self.view_tree.item(self.view_tree.selection())['text'].split("'")[1]
            Class = self.view_tree.item(self.view_tree.selection())['values'][0]
        except:
            return messagebox.showerror("Error", "No se ha seleccionado ninguna tarea")
        os.startfile(f"{self.Path}\Tareas\{Class}\{Homework}")
    #00/00/0000
    def dateformat(self,event):
        query = self.view_DateEntry.get()
        if not event.char.isdigit():
            self.view_DateEntry.delete(0, END)
            return
        if event.keysym == "BackSpace":
            return
        if len (query) == 2:
            self.view_DateEntry.insert(END, "/")
        elif len (query) == 5:
            self.view_DateEntry.insert(END, "/")
        elif len (query) == 10:
            self.view_DateEntry.delete(0, END)
            self.view_DateEntry.insert(END, query[:9])
        elif len (query) > 10:
            self.view_DateEntry.delete(0, END)
            self.view_DateEntry.insert(END, query[:10])
        
if __name__ == '__main__':
    root = Tk()
    my_menu = APP(root)
    root.mainloop()