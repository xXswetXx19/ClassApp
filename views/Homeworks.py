from tkinter import Frame, BOTH, W, E, CENTER, NO, ttk
from tkinter.ttk import Combobox, Button
from Components.multi_search import multi_search
from Core.Database import Query
from datetime import datetime



class HomeworksWindow:
    def __init__(self, toplevel, master):
        self.view_wins = toplevel
        self.query = Query()        
        self.Materias = self.query.getMateriasList()
        
        self.getWindow()
        # self.getButtons()
        self.getTreeview()
        self.getEntries()
        self.updateEntryAndTw()
        # self.query.createFakeHomeworks()
        # 
    
    def getWindow (self):
        self.view_wins.title("Tareas")
        self.view_wins.geometry("800x275")
        self.view_wins.resizable(0,0)
        self.view_wins.iconbitmap("Archivos/Icono.ico")
        
        self.view_frame = Frame(self.view_wins, bg = "#E4DFEC")
        self.view_frame.pack(expand = True, fill = BOTH)

        self.view_topframes = Frame(self.view_frame, bg = "#E4DFEC")
        self.view_topframes.grid(row = 0, column = 0, sticky = W + E)

        self.view_topframes.columnconfigure(0, minsize=200)
        self.view_topframes.columnconfigure(1, minsize=150)
        self.view_topframes.columnconfigure(2, minsize=150)
        self.view_topframes.columnconfigure(3, minsize=150)
        self.view_topframes.columnconfigure(4, minsize=150)
        
        
        self.view_buttons_frame = Frame(self.view_frame, bg = "BLUE")
        self.view_buttons_frame.grid(row= 2, column = 0, columnspan=3)
        
        self.view_buttons_frame.columnconfigure(0, minsize=200)
        self.view_buttons_frame.columnconfigure(1, minsize=200)
        self.view_buttons_frame.columnconfigure(2, minsize=200)
        self.view_buttons_frame.columnconfigure(3, minsize=200)
        
        
    def getEntries(self):    
        self.MateriasEntry = multi_search(self.view_topframes, width=10, font=('', 12), completevalues = (), Treeview = self.treeview, column = 0)
        self.MateriasEntry.grid(row = 0, column = 0,sticky = W + E)
        
        self.DocumentEntry  = multi_search(self.view_topframes, width=10, font=('', 12), completevalues = (), Treeview = self.treeview, column = 1)
        self.DocumentEntry.grid(row = 0, column = 1,sticky = W + E)
        
        self.NumEntry = multi_search(self.view_topframes, width=10, font=('', 12), completevalues = (), Treeview = self.treeview, column = 2)
        self.NumEntry.grid(row = 0, column = 2,sticky = W + E)
        
        self.DateEntry = multi_search(self.view_topframes, width=10, font=('', 12), completevalues = (), Treeview = self.treeview, column = 3)
        self.DateEntry.grid(row = 0, column = 3,sticky = W + E)

        self.TimeEntry = multi_search(self.view_topframes, width=10, font=('', 12), completevalues = (), Treeview = self.treeview, column = 4)
        self.TimeEntry.grid(row = 0, column = 4,sticky = W + E)
        
        
    def getTreeview(self):
        self.treeview = ttk.Treeview(self.view_frame, height= 10,columns = ("#1", "#2", "#3", "#4", "#5"))
        self.treeview.grid(row = 1, column = 0)
        
        self.treeview.heading('#0', text = 'ID', anchor = CENTER)
        self.treeview.heading("#1", text = 'Materia', anchor = CENTER)
        self.treeview.heading("#2", text = 'Documento', anchor = CENTER)       
        self.treeview.heading("#3", text = 'Num', anchor = CENTER)
        self.treeview.heading("#4", text = 'Fecha', anchor = CENTER)
        self.treeview.heading("#5", text = 'Hora', anchor = CENTER)
        
        self.treeview.column("#0",minwidth=0,width=0, stretch=NO, anchor= CENTER)
        self.treeview.column("#1",minwidth=100,width=200, anchor= W)
        self.treeview.column("#2",minwidth=100,width=150, anchor= CENTER)
        self.treeview.column("#3",minwidth=100,width=150, anchor= CENTER)
        self.treeview.column("#4",minwidth=100,width=150, anchor= CENTER)
        self.treeview.column("#5",minwidth=100,width=150, anchor= CENTER)



    # def getButtons(self):
    #     ButtonsData = {
    #         "Eliminar": lambda: DeleteHomework(self), 
    #         "Ubicacion": lambda: OpenPath(self), 
    #         "Abrir": lambda: OpenHomework(self),
    #         "PDF": lambda: DoctoPdf(self)}
        
    #     for i in range(len(ButtonsData.keys())):
    #         btn = Button(self.view_buttons_frame, text = list(ButtonsData.keys())[i], command= list(ButtonsData.values())[i], width=10, height=1)
    #         btn.grid(row = 0, column = i, sticky = W + E)

    #     self.treeview.tag_configure('Tareas', font=("", 10), foreground = 'Black')
    #     getHomeworks(self)


    def updateEntryAndTw (self):
        Homeworks = self.query.getHomeworksList()
        Documents = [i[2] for i in Homeworks]
        Num = []
        Date = []
        Time = []
        Materias = self.query.getMateriasList()

        Lista_organizada = []
        num = self.query.run_query("SELECT COUNT(*) AS NumTareas FROM Tarea GROUP BY DATE(FechaHora) ORDER BY NumTareas DESC LIMIT 1").fetchall()[0][0]
        for i in range(num):
            Num.append(str(i+1))
            
        for i in Homeworks:
            # i[1] is datetime string
            Datetime = datetime.strptime(i[4], '%Y-%m-%d %H:%M:%S')
            DateV = Datetime.strftime('%d/%m/%Y')
            TimeV = Datetime.strftime('%H:%M:%S')
            Date.append(DateV)
            Time.append(TimeV)
            
            Lista_organizada.append([i[0], i[1], i[2], i[3], DateV, TimeV])
            
        Lista_organizada = sorted(Lista_organizada, key=lambda x: x[0])
        
        self.MateriasEntry.set_column_completion_list(Materias)
        self.DocumentEntry.set_column_completion_list(Documents)
        self.NumEntry.set_column_completion_list(Num)
        self.DateEntry.set_column_completion_list(Date)
        self.TimeEntry.set_column_completion_list(Time)
        
        
        self.MateriasEntry.set_tw_completion_list(Lista_organizada)
        self.DocumentEntry.set_tw_completion_list(Lista_organizada)
        self.NumEntry.set_tw_completion_list(Lista_organizada)
        self.DateEntry.set_tw_completion_list(Lista_organizada)
        self.TimeEntry.set_tw_completion_list(Lista_organizada)
        