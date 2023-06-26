from tkinter import Frame, Button, Label, Entry, W, E, CENTER, BOTH, LEFT, NO, ttk, Toplevel, messagebox
from Clibs.Autocomplete import AutocompleteCombobox
from Procesos.Configuracion import getHomeworks, DeleteHomework, OpenHomework, OpenPath
from Procesos.General import FillTw, updateList, CreateDirs, CreateTarea, clearTw, clearviewTw,removeMateria
from Procesos.Principales import getPath, getMaterias, CreateDirs
from views.Calendary import calendar
from views.Config import ConfigWin
from views.Tareas import HomeworksWindow
from views.addMateria import addMateriaView

class APP:
    def __init__(self, master):
        self.master = master
        self.open_windows = {}
        
        self.views = {
            "Tareas": HomeworksWindow,
            "Calendario": calendar,
            "Configuracion": ConfigWin,
            "Agregar_Materia": addMateriaView
        }


        self.getWindow()
        self.getButtons()
        self.getEntries()
        self.getTreeviewer()
        FillTw(self)
        updateList(self)
    
    def getWindow(self):
        self.master.title("Gestor de tareas")
        self.master.geometry("521x248")
        self.master.resizable(0,0)
        self.master.iconbitmap("Archivos/Icono.ico")
    
        # Creating Frames
        self.TWframe = Frame(self.master)
        self.frame = Frame(self.master)
        
        # Packing Frames
        self.TWframe.pack(expand = True, fill = BOTH, side=LEFT)
        self.frame.pack(expand=True, fill=BOTH, side=LEFT)
    




    def getButtons(self):
        ButtonsData = {
            "Crear Tarea": lambda: CreateTarea(self),
            "Ver Tareas": lambda: self.open_view("Tareas"),
            "Calendario": lambda: self.open_view("Calendario"),
            "Configuracion":  lambda: self.open_view("Configuracion"),
            "Agregar Materia": lambda: self.open_view("Agregar_Materia"),
            "Eliminar Materia": lambda: removeMateria(self),
            "Salir": self.master.destroy
            # "Ver Pendientes": Pendientes,
        }
        # Creating Buttons
        for i in range(len(ButtonsData.keys())):
            Button(self.frame, text = list(ButtonsData.keys())[i], command = list(ButtonsData.values())[i], width=30).pack(fill=BOTH, expand=True)
        
    def getEntries(self):
        # Creating Search Bar and placing it
        self.entry = AutocompleteCombobox(self.TWframe, width=25,completevalues = lambda: [])
        self.entry.grid(row = 0, column = 0,sticky = W + E)
        
        # Event binds
        self.entry.bind('<KeyPress>', self.__update)
        self.entry.bind("<FocusIn>", self.__update)
    
    def getTreeviewer(self):
        # Creating Treeview and placing it
        self.tree = ttk.Treeview(self.TWframe, height= 10,columns = 2)
        self.tree.grid(row = 2, column = 0)
        self.tree.heading('#0', text = 'ID', anchor = CENTER)
        self.tree.column("#0",minwidth=0,width=0, stretch=NO, anchor= CENTER)
        self.tree.heading('#1', text = 'Materias', anchor = CENTER)
        self.tree.column("#1",minwidth=100,width=300, anchor= CENTER)
        # Treeview Configuration
        self.tree.tag_configure('Materias', font=("", 10), foreground = 'Black')
        


    def open_view(self, tipo):
        if tipo in self.open_windows:
            self.open_windows[tipo].lift()
            return messagebox.showerror("Error", "Ya hay una ventana de calendario abierta")
            
            
        ventana_actual = Toplevel(self.master)
        self.open_windows[tipo] = ventana_actual
        ventana_actual.protocol("WM_DELETE_WINDOW", lambda: self.close_view(tipo))
            
        clase = self.views[tipo]
        vista_instance = clase(ventana_actual)

    def close_view(self, tipo):
        ventana_actual = self.open_windows.pop(tipo, None)
        if ventana_actual:
            ventana_actual.destroy()
            
            
            
            
            
            
    
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
