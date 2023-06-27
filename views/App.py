from tkinter import Frame, Button, W, E, CENTER, BOTH, LEFT, NO, ttk, Toplevel, messagebox
from Components.auto_search import auto_searchTw
from views.Calendary import calendar
from views.Config import ConfigWin
from views.Homeworks import HomeworksWindow
from views.addMateria import addMateriaView
from Procesos.Homeworks import HomeworkProcess
from Core.Database import Query

class APP:
    def __init__(self, master):
        self.master = master
        self.open_windows = {}
        self.query = Query()
        
        self.views = {
            "Tareas": HomeworksWindow,
            "Calendario": calendar,
            "Configuracion": ConfigWin,
            "Agregar_Materia": addMateriaView
        }

        self.getWindow()
        self.getButtons()
        self.getTreeviewer()
        self.getEntries()
        
        self.TreeviewProcess = HomeworkProcess(self.entry)

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
            "Crear Tarea": lambda: self.TreeviewProcess.CreateTarea(),
            "Ver Tareas": lambda: self.open_view("Tareas"),
            "Calendario": lambda: self.open_view("Calendario"),
            "Configuracion":  lambda: self.open_view("Configuracion"),
            "Agregar Materia": lambda: self.open_view("Agregar_Materia"),
            "Eliminar Materia": lambda: self.TreeviewProcess.removeMateria(),
            "Salir": self.master.destroy
            # "Ver Pendientes": Pendientes,
        }
        # Creating Buttons
        for i in range(len(ButtonsData.keys())):
            Button(self.frame, text = list(ButtonsData.keys())[i], command = list(ButtonsData.values())[i], width=30).pack(fill=BOTH, expand=True)
        
    def getEntries(self):
        values = self.query.getMateriasList()
        self.entry = auto_searchTw(self.TWframe, width=25,completevalues = values, Treeview=self.tree)
        self.entry.grid(row = 0, column = 0,sticky = W + E)
    
    
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
            messagebox.showerror("Error", "Ya hay una ventana de calendario abierta")
            return self.open_windows[tipo].lift()
        ventana_actual = Toplevel(self.master)
        self.open_windows[tipo] = ventana_actual
        ventana_actual.protocol("WM_DELETE_WINDOW", lambda: close_view(tipo))
            
        clase = self.views[tipo]
        vista_instance = clase(ventana_actual, self)

        def close_view(tipo):
            ventana_actual = self.open_windows.pop(tipo, None)
            if ventana_actual:
                ventana_actual.destroy()
            
    
    
