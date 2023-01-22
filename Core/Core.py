from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkinter.ttk import Combobox
from Clibs import Autocomplete as ac
import Clibs.calendario as cal
from Core.Database import *
from Procesos.General import *
from Procesos.Principales import getPath, getMaterias

class Core:
    def __init__(self):
        self.master = Tk()


    def start(self):
        self.startDatabase()
        self.App = APP(self.master)
        self.master.mainloop()

    def startDatabase(self):
        createDB()
        createTableMaterias()
        createTableConfig()
        createTableCantidad()
        createTableNotas()
    
    # ! Intentar reemplazar
    def opencal(self):
            calwin = Toplevel(self.master)
            cal.Calendario(calwin)


    def VerTareas(self):
        if any(isinstance(x, Toplevel) for x in self.master.winfo_children()):
            if self.view_wins.winfo_exists() if self.view_wins.winfo_exists() else False:
                messagebox.showerror("Error", "Ya hay un visualizador de tareas abierto")
                return self.view_wins.lift() 
        self.view_wins = Toplevel(self.master)
        self.view_win_functions = HomeworksWindow(self.view_wins)
    
    def configuration(self):
        if any(isinstance(x, Toplevel) for x in self.master.winfo_children()):
            if (self.config_win.winfo_exists() if self.config_win.winfo_exists() else False):
                messagebox.showerror("Error", "Ya hay una ventana de configuracion abierta")
                return self.config_win.lift() 
        self.config_win = Toplevel(self.master)
        ConfigWin(self.config_win)


class APP:
    def __init__(self, master):
        # Window config
        self.master = master
        self.master.title("Gestor de tareas")
        self.master.geometry("521x248")
        self.master.resizable(0,0)
        # self.master.iconbitmap("Icono.ico")

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
        # ! Agregar lista de materias
        self.entry = ac.AutocompleteCombobox(self.TWframe, width=25,completevalues = lambda: [])
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
            "Crear Tarea": lambda: CreateTarea(self),
            "Ver Tareas": lambda: HomeworksWindow(Toplevel(self.master)),
            "Calendario": lambda: cal.Calendario(Toplevel(self.master)),
            # "Ver Pendientes": Pendientes,
            "Configuracion":  lambda:ConfigWin(Toplevel(self.master)),
            "Agregar Materia": lambda: addMateria(self),
            "Eliminar Materia": lambda: removeMateria(self),
            "Salir": self.master.destroy
        }
        # Creating Buttons
        for i in range(len(ButtonsData.keys())):
            Button(self.frame, text = list(ButtonsData.keys())[i], command = list(ButtonsData.values())[i], width=30).pack(fill=BOTH, expand=True)
        # Startup Functions
        FillTw(self)
        updateList(self)
    
    
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
            FillTw(self)
            for child in self.tree.get_children():
                if self.tree.item(child)['values']:
                    if str(query.lower()) in self.tree.item(child)['values'][0].lower():
                        selections.append(child)
            for child in self.tree.get_children():
                if child not in selections:
                    self.tree.detach(child)
        else:
            FillTw(self)
        if len(selections) == 1:
            self.tree.selection_set(selections)



class ConfigWin:
    def __init__(self, toplevel):
        self.Config_win = toplevel
        self.Config_win.resizable(width=False, height=False)
        self.Config_win.title = 'Configuración'
        self.Config_win.geometry('500x150')
        # self.Config_win.iconbitmap("Icono.ico")
        Path = getPath()
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
        # getPath()
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
        # getPath()
    def browsedir(self):
        Dirname = filedialog.askdirectory()
        if Dirname:
            self.RutaEntry["textvariable"] = StringVar(self.Config_win, value = Dirname)  

class HomeworksWindow:
    def __init__(self, toplevel):
        self.view_wins = toplevel
        self.view_wins.title("Tareas")
        self.view_wins.geometry("650x275")
        self.view_wins.resizable(0,0)
        self.view_wins.config(bg = "")
        # self.view_wins.iconbitmap("Icono.ico")
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

        ButtonsData = { "Eliminar": lambda: DeleteHomework(self), "Ubicacion": lambda: OpenPath(self), "Abrir": lambda: OpenHomework(self) }
        for i in range(len(ButtonsData.keys())):
            Button(self.view_buttons_frame, text = list(ButtonsData.keys())[i], command= list(ButtonsData.values())[i], width=10, height=1).grid(row = 0, column = i, sticky = W + E)

        self.view_tree.tag_configure('Tareas', font=("", 10), foreground = 'Black')
        # Startup functions
        # getPath()
        getHomeworks(self)

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
            getHomeworks(self)
            for child in self.view_tree.get_children():
                if self.view_tree.item(child)['values']:
                    if query.lower() in str(self.view_tree.item(child)['values'][index]).lower():
                        selections.append(child)
            for child in self.view_tree.get_children():
                if child not in selections:
                    self.view_tree.detach(child)
        else:
            getHomeworks(self)

class VerPendientes:
    def __init__(self):
        self.win = Toplevel()
        self.win.title("Tareas")
        self.win.geometry("300x400")
        # self.win.resizable(0,0)
        color1 = "#eeeeee"
        self.HomeworksFrame = Frame(self.win, bg=color1, bd=4, relief="ridge", width=300, height=400)
        self.HomeworksFrame.grid(row=1, column=0, sticky=NSEW)
        self.listcolors = ["#ffffff", "#eeeeee", "#dddddd", "#cccccc", "#bbbbbb", "#aaaaaa", "#999999", "#888888", "#777777", "#666666", "#555555", "#444444", "#333333", "#222222", "#111111", "#000000"]
        self.FillPending()
    def FillPending(self):
        for i, color in enumerate(self.listcolors):
            Label(self.HomeworksFrame, text = "Hola", bg = color).grid(row = i, column = 0)

        