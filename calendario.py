from tkinter import *
from tkinter import ttk, messagebox
import calendar
from datetime import date
import sqlite3

def create_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Notas (
                id INTEGER PRIMARY KEY,
                dia INTEGER,
                mes INTEGER,
                año INTEGER,
                descripcion TEXT,
                prioridad TEXT
                )""")
    conn.commit()
    conn.close()
def run_query(query, parameters=()):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result

def insert_db(dia, mes, año, descripcion, prioridad):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Notas VALUES (NULL, ?, ?, ?, ?, ?)", (dia, mes, año, descripcion, prioridad))
    conn.commit()
    conn.close()

def delete_Nota(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM Notas WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def search_DayData(**kwargs):
    Id = kwargs.get('Id', None)
    if Id:
        rows = run_query("SELECT * FROM Notas WHERE id = ?", (Id,)).fetchone()
        return rows if len(rows) != 0 else None
    else:
        dia = kwargs.get('dia', None)
        mes = kwargs.get('mes', None)
        año = kwargs.get('año', None)
        rows = run_query("SELECT * FROM Notas WHERE dia = ? AND mes = ? AND año = ?", (dia, mes, año)).fetchall()
        return rows if len(rows) != 0 else None

create_db()

class Dia(Label):
    def __init__(self, *args, **kwargs):
        date = kwargs.pop('date', None)
        super().__init__(*args,**kwargs)
        self.Dia = date.day
        self.Mes = date.month
        self.Año = date.year
        
        self.__Notas = []
        self.updateDayData()
        
    def addNota(self, descripcion):
        self.__Notas.append(descripcion)
    def getDescripcion(self):
        self.__Notas.sort(key=lambda x: ["Baja", "Media", "Alta","Urgente"].index(x[1]), reverse=True)
        return self.__Notas
    def getday(self):
        return self.Dia
    def getmonth(self):
        return self.Mes
    def getyear(self):
        return self.Año
    def updateDayData(self):
        DayData = search_DayData(dia=self.Dia, mes=self.Mes, año=self.Año)
        self.__Notas = []
        if DayData:
            for Data in DayData:
                Id, dia, mes, año, descripcion, prioridad = Data
                self.__Notas.append([Id, prioridad, descripcion])

class Ventanita:
    def __init__(self, calendario, widgetday):
        win = Toplevel()
        win.title("Tareas")
        win.geometry("400x200")
        win.resizable(0,0)
        self.win = win
        self.Diaclass = widgetday
        self.calendario = calendario
        color1 = "#eeeeee"
        self.TopFrame = Frame(win, bg=color1)
        self.ButtonsFrame = Frame(win)
        self.HomeworksFrame = Frame(self.TopFrame, bg=color1, bd=4, relief="ridge", width=400, height=150)
    
        self.TopFrame.pack(expand= True, fill=BOTH, side=TOP)
        self.HomeworksFrame.grid(row=1, column=0, sticky=NSEW)
        self.ButtonsFrame.pack(fill=BOTH, side=BOTTOM)

        self.TopFrame.grid_rowconfigure(1, minsize=150)
        self.TopFrame.grid_columnconfigure(0, minsize=400)

        Toptext = f"Tareas del {self.Diaclass.getday()}/{self.Diaclass.getmonth()}/{self.Diaclass.getyear()}"
        Daynum = Label(self.TopFrame, text= Toptext, font=("Arial", 11, "bold"), background=color1)
        Daynum.grid(row=0, column=0, sticky= NSEW)
        
        self.view_tree = ttk.Treeview(self.HomeworksFrame, height= 6,columns = ["#0", "#1"])
        self.view_tree.grid(row = 0, column = 0)
        self.view_tree.heading("#0", text = "ID")
        self.view_tree.heading("#1", text = "Descripción")
        self.view_tree.heading("#2", text = "Prioridad")
        
        self.view_tree.column("#0", width=0,minwidth=0)
        self.view_tree.column("#1", width = 322, anchor=W)
        self.view_tree.column("#2", width = 70, anchor="center")
        
        # Creando los tags
        self.view_tree.tag_configure("Baja", background=calendario.Colores.get("Baja"))
        self.view_tree.tag_configure("Media", background=calendario.Colores.get("Media"))
        self.view_tree.tag_configure("Alta", background=calendario.Colores.get("Alta"))
        self.view_tree.tag_configure("Urgente", background=calendario.Colores.get("Urgente"))
 
        Button(self.ButtonsFrame, text="Añadir Pendiente", font=("Arial", 11, "bold"), background=color1, command=self.addNota, width=20).pack(side=LEFT)
        Button(self.ButtonsFrame, text="Eliminar Pendiente", font=("Arial", 11, "bold"), background=color1, command=self.deleteNota, width=25).pack(side=RIGHT)
        self.fill_tree()
    def clear_tree(self):
        self.view_tree.delete(*self.view_tree.get_children())
    def fill_tree(self):
        self.clear_tree()
        self.Diaclass.updateDayData()
        for Id, Prioridad, Nota in self.Diaclass.getDescripcion():
            row = self.view_tree.insert("", "end", text=Id, values=[Nota, Prioridad])
            if Prioridad == "Baja":
                self.view_tree.item(row, tags="Baja")
            elif Prioridad == "Media":
                self.view_tree.item(row, tags="Media")
            elif Prioridad == "Alta":
                self.view_tree.item(row, tags="Alta")
            elif Prioridad == "Urgente":
                self.view_tree.item(row, tags="Urgente")
    def addNota(self):
        # if any(isinstance(x, Toplevel) for x in self.master.winfo_children()):
        #     if self.Add_win.winfo_exists() if self.Add_win.winfo_exists() else False:
        #         messagebox.showerror("Error", "Ya hay una ventana")
        #         return self.Add_win.lift() 
        self.Add_win = Toplevel()
        self.Add_win.resizable(width=False, height=False)
        self.Add_win.title = 'Agregar Nota'
        self.Add_win.geometry('300x200')
        self.Add_win.iconbitmap("Icono.ico")
        def agg(Descripcion, Prioridad):
            if Descripcion == "":  
                return messagebox.showerror("Error", "No has ingresado una descripción")
            day = self.Diaclass.getday()
            month = self.Diaclass.getmonth()
            year = self.Diaclass.getyear()
            insert_db(day, month, year, Descripcion, Prioridad)
            self.calendario.filldays(month, year)
            self.fill_tree()
            
            self.Add_win.destroy()
        LDescripcion = Label(self.Add_win, text = 'Descripcion: ')
        LDescripcion.place(anchor = CENTER, relx = .2, rely = .3)
        CDescripcion = Entry(self.Add_win, width=25)
        CDescripcion.place(anchor = CENTER, relx = .6, rely = .3)
        LPrioridad = Label(self.Add_win, text = 'Prioridad: ')
        LPrioridad.place(anchor = CENTER, relx = .2, rely = .5)
        CPrioridad = ttk.Combobox(self.Add_win, values = ['Baja', 'Media', 'Alta', 'Urgente'], width=22, state="readonly", justify=CENTER)
        CPrioridad.place(anchor = CENTER, relx = .6, rely = .5)
        CPrioridad.current(0)
        Boton = Button(self.Add_win, text = 'Agregar', command = lambda: agg(CDescripcion.get(), CPrioridad.get()))
        Boton.place(anchor = CENTER, relx = .5, rely = .7)
        self.Add_win.bind('<Return>', lambda event: agg(CDescripcion.get(), CPrioridad.get()))
        
    def deleteNota(self):
        Id = self.view_tree.item(self.view_tree.selection())['text']
        if not Id:
            messagebox.showerror("Error", "No se ha seleccionado ninguna tarea")
            return self.win.lift()
        ask = messagebox.askyesno("Eliminar", "¿Esta seguro de eliminar la Nota?")
        if ask:
            Data = search_DayData(Id = Id)
            Id, dia, mes, año, Descripcion, Prioridad = Data
            delete_Nota(Id)
            self.calendario.filldays(mes, año)
            self.fill_tree()


class Calendario:
    def __init__ (self, window):
# Crea la ventana principal y el calendario
        self.window = window
        self.window.geometry("755x375")
        self.window.title("Calendario")
        self.window.resizable(0,0)
        self.TopFrame = Frame(self.window,background="#006064", height=50)
        self.CenterFrame = Frame(self.window, background="black", height=30)
        self.BotFrame = Frame(self.window, height=205)
        # Frames
        self.TopFrame.pack(fill = BOTH, side=TOP)
        self.CenterFrame.pack(fill = BOTH, side=TOP)
        self.BotFrame.pack(fill=BOTH, side=TOP)
        
        # Mehh 
        self.Colores = {
            "Baja": "#99e5b1", # M
            "Media": "#d4b98d",
            "Alta": "#c78989",
            "Urgente": "#d32f2f"
        } 
        
        self.Meses = {
            "January": "Enero",
            "February": "Febrero",
            "March": "Marzo",
            "April": "Abril",
            "May": "Mayo",
            "June": "Junio",
            "July": "Julio",
            "August": "Agosto",
            "September": "Septiembre",
            "October": "Octubre",
            "November": "Noviembre",
            "December": "Diciembre"
        }

        # Terracota
        # self.Colores = {
        #     "Baja": "#88d8b0",
        #     "Media": "#c9b57d",
        #     "Alta": "#b78787",
        #     "Urgente": "#c62828"
        # }
        # Puede ser
        # self.Colores = {
        #     "Baja": "#77bf9f",
        #     "Media": "#b8a27c",
        #     "Alta": "#a67676",
        #     "Urgente": "#b71b1c"
        # }
        # self.Colores = {
        #     "Baja": "#66a68f",
        #     "Media": "#a79773",
        #     "Alta": "#966362",
        #     "Urgente": "#a30000"
        # }
        # Fuertes
        # self.Colores = {
        #     "Baja": "#00b200",
        #     "Media": "#e6a800",
        #     "Alta": "#cc3333",
        #     "Urgente": "#ff0000"
        # }
        # Fuertes y claros
        # self.Colores = {
        #     "Baja": "#33cc33",
        #     "Media": "#ffff00",
        #     "Alta": "#ff9933",
        #     "Urgente": "#ff3333"
        # }
        
        # Top Frame
        self.butt1 = Label(self.TopFrame, text = "<",width= 5, height=3, font=(10), background= "#006064", foreground= "white")
        self.butt1.pack(side = LEFT, anchor=CENTER)
        self.butt2 = Label(self.TopFrame, text = ">", width= 5, height=3, font=(10), background= "#006064", foreground= "white")
        self.butt2.pack(side = RIGHT, anchor=CENTER)
        self.MesLabel = Label(self.TopFrame, text= "",background="#006064",foreground= "#FFFFFF", font=("Arial Black", 21))
        self.MesLabel.pack(anchor=CENTER, expand=True)
        self.butt1.bind("<Button-1>", self.previousmonth)
        self.butt2.bind("<Button-1>", self.nextmonth)
        self.butt1.bind("<Enter>", lambda event: self.butt1.config(background="#004d4d"))
        self.butt1.bind("<Leave>", lambda event: self.butt1.config(background="#006064"))
        self.butt2.bind("<Enter>", lambda event: self.butt2.config(background="#004d4d"))
        self.butt2.bind("<Leave>", lambda event: self.butt2.config(background="#006064"))
        # Center Frame
        Dias = ("Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo")
        for i, dia in enumerate(Dias):
            Label(self.CenterFrame,background="#006064",text=dia, font=("Arial", 11, "bold"), foreground= "#FFFFFF", width=10, height=2, border= 8).grid(row=0, column=i)
        # Crea el widget Calendar
        self.mes_actual = date.today().month
        self.ano_actual = date.today().year
        self.MesLabel.config(text = self.Meses[date(self.ano_actual, self.mes_actual, 1).strftime("%B")] + " " + str(self.ano_actual))
        self.filldays(self.mes_actual, self.ano_actual)
        
    def filldays(self, month, year):
        c = calendar.Calendar(firstweekday=calendar.MONDAY)
        cal = c.monthdatescalendar(year, month)
        self.clearcalendar()
        label_cant = 0
        for i, week in enumerate(cal):
            for j, date in enumerate(week):
                if date.month == month: 
                    label = Dia(self.BotFrame, text=date.day, bg="#eeeeee", font="Arial 11", width=10, height=2, border=8, date=date)
                    label.grid(row=i, column=j)
                    label_cant += 1
                    if len(label.getDescripcion()) > 0:
                        prioridad = label.getDescripcion()[0][1]
                        Color = self.Colores.get(prioridad)
                        label.config(background=Color)
                    label.bind("<Button-1>", self.on_click)
                    label.bind("<Button-3>", self.on_click)
                    label.bind("<Enter>", self.onover)
                    label.bind("<Leave>", self.onleave)
                else:
                    label = Dia(self.BotFrame, text=date.day, bg="#D3D3D3", fg="#808080", font="Arial 11", width=10, height=2, border=8, date=date)
                    label.grid(row=i, column=j)
                    label_cant += 1
                    if date.month < month and date.year == self.ano_actual or date.month < month and date.year < self.ano_actual or date.month > month and date.year < self.ano_actual:
                        label.bind("<Button-1>", self.previousmonth)
                    else:
                        label.bind("<Button-1>", self.nextmonth)
            if label_cant > 35:
                self.window.geometry("755x425")
            else:   
                self.window.geometry("755x375")                     
    def clearcalendar(self):
        for widget in self.BotFrame.winfo_children():
             widget.destroy()
    def previousmonth(self, event):
        month = self.mes_actual - 1
        if month == 0:
            self.ano_actual -= 1
            month = 12
        if type (event.widget["text"]) == int:
            self.MesLabel.config(text = self.Meses[date(self.ano_actual, month, 1).strftime("%B")] + " " + str(self.ano_actual))
            self.filldays(month, self.ano_actual)
        else:
            self.filldays(month, self.ano_actual)
            self.MesLabel.config(text = self.Meses[date(self.ano_actual, month, 1).strftime("%B")] + " " + str(self.ano_actual))
        self.mes_actual = month
    def nextmonth(self, event):
        month = self.mes_actual + 1
        if month == 13:
            self.ano_actual += 1
            month = 1
        if type (event.widget["text"]) == int:
            self.MesLabel.config(text = self.Meses[date(self.ano_actual, month, 1).strftime("%B")] + " " + str(self.ano_actual))
            self.filldays(month, self.ano_actual)
        else:
            self.filldays(month, self.ano_actual)
            self.MesLabel.config(text = self.Meses[date(self.ano_actual, month, 1).strftime("%B")] + " " + str(self.ano_actual))
        self.mes_actual = month
        
    def on_click(self, event):
        label = event.widget
        Ventanita(self, label)
    def onover(self, event):
        label = event.widget
        if label["background"] == "#eeeeee":
          label.config(background="#c3c3c3")
    def onleave(self, event):
        label = event.widget
        if label["background"] == "#c3c3c3":
            label.config(background="#eeeeee")