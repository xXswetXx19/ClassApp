from tkinter import Frame, BOTH, W, E, CENTER, NO, Entry, ttk
from tkinter.ttk import Combobox, Button




class HomeworksWindow:
    def __init__(self, toplevel):
        self.view_wins = toplevel
        self.view_wins.title("Tareas")
        self.view_wins.geometry("800x275")
        self.view_wins.resizable(0,0)
        self.view_wins.iconbitmap("Archivos/Icono.ico")
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
        self.view_topframes.columnconfigure(4, minsize=150)
        
        for i in range(4):
            Entry(self.view_topframes, width=10, font=('', 12)).grid(row = 0, column = i + 1,sticky = W + E)
        # Getting the entries from a frame and giving events to them
        self.entries = [i for i in self.view_topframes.children.values() if type(i) == Entry or type(i) == Combobox]
        for index, entrie in enumerate(self.entries):
            entrie.bind("<KeyPress>", lambda event, entry = entrie, index = index: self.filterupdate(event, entry, index))
            entrie.bind("<FocusIn>", lambda event, entry = entrie, index = index: self.filterupdate(event, entry, index))
        
        # Creating Treeview
        self.view_tree = ttk.Treeview(self.view_frame, height= 10,columns = ("#1", "#2", "#3", "#4", "#5"))
        self.view_tree.grid(row = 1, column = 0)
        
        self.view_tree.heading('#0', text = 'ID', anchor = CENTER)
        self.view_tree.heading("#1", text = 'Materia', anchor = CENTER)
        self.view_tree.heading("#2", text = 'Documento', anchor = CENTER)       
        self.view_tree.heading("#3", text = 'Num', anchor = CENTER)
        self.view_tree.heading("#4", text = 'Fecha', anchor = CENTER)
        self.view_tree.heading("#5", text = 'Hora', anchor = CENTER)
        
        self.view_tree.column("#0",minwidth=0,width=0, stretch=NO, anchor= CENTER)
        self.view_tree.column("#1",minwidth=100,width=200, anchor= W)
        self.view_tree.column("#2",minwidth=100,width=150, anchor= CENTER)
        self.view_tree.column("#3",minwidth=100,width=150, anchor= CENTER)
        self.view_tree.column("#4",minwidth=100,width=150, anchor= CENTER)
        self.view_tree.column("#5",minwidth=100,width=150, anchor= CENTER)

        self.view_buttons_frame = Frame(self.view_frame, bg = "BLUE")
        self.view_buttons_frame.grid(row= 2, column = 0, columnspan=3)
        
        self.view_buttons_frame.columnconfigure(0, minsize=200)
        self.view_buttons_frame.columnconfigure(1, minsize=200)
        self.view_buttons_frame.columnconfigure(2, minsize=200)
        self.view_buttons_frame.columnconfigure(3, minsize=200)

        ButtonsData = { 
            "Eliminar": lambda: DeleteHomework(self), 
            "Ubicacion": lambda: OpenPath(self), 
            "Abrir": lambda: OpenHomework(self),
            "PDF": lambda: DoctoPdf(self)}
        
        for i in range(len(ButtonsData.keys())):
            Button(self.view_buttons_frame, text = list(ButtonsData.keys())[i], command= list(ButtonsData.values())[i], width=10, height=1).grid(row = 0, column = i, sticky = W + E)

        self.view_tree.tag_configure('Tareas', font=("", 10), foreground = 'Black')
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