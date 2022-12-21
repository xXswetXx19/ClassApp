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

def view_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Notas")
    rows = c.fetchall()
    conn.close()
    return rows

def delete_db(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM Notas WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def update_db(id, dia, mes, año, descripcion, prioridad):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE Notas SET dia = ?, mes = ?, año = ?, descripcion = ?, prioridad = ? WHERE id = ?", (dia, mes, año, descripcion, prioridad, id))
    conn.commit()
    conn.close()

def search_db(dia="", mes="", año="", descripcion="", prioridad=""):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Notas WHERE dia = ? OR mes = ? OR año = ? OR descripcion = ? OR prioridad = ?", (dia, mes, año, descripcion, prioridad))
    rows = c.fetchall()
    conn.close()
    return rows
def get_Dias():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Notas")
    rows = c.fetchall()
    conn.close()
    return rows
create_db()

class Dia(Label):
    def __init__(self, *args, **kwargs):
        date = kwargs.pop('date', None)
        Id = kwargs.pop('Id', None)
        super().__init__(*args,**kwargs)
        self.Id = Id
        self.Dia = date.day
        self.Mes = date.month
        self.Año = date.year
        self.Fecha = date

        self.__Notas = [
            ["Urgente", "Ir al Tuti"],
            ["Baja", "Hacer mates"],
            ["Baja", "Hacer Dominar el sss"],
            ["Media", "Dominar el mundo"],
            ["Alta", "Perriar hasta el piso"],
            ["Baja", "Wacamole"],
            ["Alta", "Hacer la tarea"],
            ["Urgente", "Ir al doctor"]
        ]
    def addNota(self, descripcion):
        self.__Notas.append(descripcion)
    def getDescripcion(self):
        self.__Notas.sort(key=lambda x: ["Baja", "Media", "Alta","Urgente"].index(x[0]), reverse=True)
        return self.__Notas
    def getday(self):
        return self.Dia
    def getmonth(self):
        return self.Mes
    def getyear(self):
        return self.Año
    def getFecha(self):
        return self.Fecha
    def getid(self):
        return self.Id

class Ventanita:
    def __init__(self, widgetday):
        win = Toplevel()
        win.title("Tareas")
        win.geometry("400x200")
        win.resizable(0,0)
        self.Diaclass = widgetday
        color1 = "#eeeeee"
        color2 = "#F5F5DC"
        self.TopFrame = Frame(win, bg=color1)
        self.ButtonsFrame = Frame(win, bg="red")
        self.HomeworksFrame = Frame(self.TopFrame, bg=color1, bd=4, relief="ridge", width=400, height=150)
    
        self.TopFrame.pack(expand= True, fill=BOTH, side=TOP)
        self.HomeworksFrame.grid(row=1, column=0, sticky=NSEW)
        self.ButtonsFrame.pack(fill=BOTH, side=BOTTOM)

        self.TopFrame.grid_rowconfigure(1, minsize=150)
        self.TopFrame.grid_columnconfigure(0, minsize=400)

        Toptext = f"Tareas del {self.Diaclass.getday()}/{self.Diaclass.getmonth()}/{self.Diaclass.getyear()}"
        Daynum = Label(self.TopFrame, text= Toptext, font=("Arial", 11, "bold"), background=color1)
        Daynum.grid(row=0, column=0, sticky= NSEW)
        
        self.view_tree = ttk.Treeview(self.HomeworksFrame, height= 6,columns = 2)
        self.view_tree.grid(row = 0, column = 0)
        self.view_tree.heading("#0", text = "Descripción")
        self.view_tree.heading("#1", text = "Prioridad")
        self.view_tree.column("#0", width = 320, anchor=W)
        self.view_tree.column("#1", width = 70, anchor="center")
        
        # Creando los tags
        self.view_tree.tag_configure("Baja", background="#D5F5E3")
        self.view_tree.tag_configure("Media", background="#F5E6C0")
        self.view_tree.tag_configure("Alta", background="#E6B0AA")
        self.view_tree.tag_configure("Urgente", background="#FF5252")
        
        # Ponerle bordes a las filas del treeview
        for Prioridad, Nota in self.Diaclass.getDescripcion():
            row = self.view_tree.insert("", "end", text=Nota, values=Prioridad)
            if Prioridad == "Baja":
                self.view_tree.item(row, tags="Baja")
            elif Prioridad == "Media":
                self.view_tree.item(row, tags="Media")
            elif Prioridad == "Alta":
                self.view_tree.item(row, tags="Alta")
            elif Prioridad == "Urgente":
                self.view_tree.item(row, tags="Urgente")
            
        Button(self.ButtonsFrame, text="Añadir Pendiente", font=("Arial", 11, "bold"), background=color1, command=self.addNota, width=20).pack(side=LEFT)
        Button(self.ButtonsFrame, text="Eliminar Pendiente", font=("Arial", 11, "bold"), background=color1, command=(), width=25).pack(side=RIGHT)
   
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
        Id = self.view_tree.selection()[0]
        self.view_tree.delete(Id)
        
class Calendario:
    def __init__ (self, window):
# Crea la ventana principal y el calendario
        self.window = window
        self.window.geometry("755x375")
        self.window.title("Calendario")
        self.window.resizable(0,0)
        self.TopFrame = Frame(self.window,background="#006064", height=50)
        self.CenterFrame = Frame(self.window, background="black", height=30)
        self.BotFrame = Frame(self.window,background="red", height=205)
        # Frames
        self.TopFrame.pack(fill = BOTH, side=TOP)
        self.CenterFrame.pack(fill = BOTH, side=TOP)
        self.BotFrame.pack(fill=BOTH, side=BOTTOM)
        

        self.Colores = {
            "Baja": "#D5F5E3",
            "Media": "#F5E6C0",
            "Alta": "#E6B0AA",
            "Urgente": "#FF5252"
        } 
        

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
        self.MesLabel.config(text=date(self.ano_actual, self.mes_actual, 1).strftime("%B %Y"))

        self.c = calendar.Calendar(firstweekday=calendar.MONDAY)
        self.filldays(self.c.monthdatescalendar(2022, self.mes_actual), self.mes_actual)

    

    def filldays(self, cal, month):
        self.clearcalendar()
        db_result = get_Dias()
        for i, week in enumerate(cal):
            for j, day in enumerate(week):
                #! try:
                #!     if db_result[j]:
                #!         Id, dia, mes, año, descripcion, prioridad = db_result[j]
                #!         print(Id, dia, mes, año, descripcion, prioridad)
                #! except:
                #!     pass

                if day.month == month: 
                    label = Dia(self.BotFrame, text=day.day, bg="#eeeeee", font="Arial 11", width=10, height=2, border=8, date=day)
                    label.grid(row=i, column=j)
                    
                    imp = label.getDescripcion()[0][0]
                    Color = self.Colores[imp]
                    label.config(background=Color)
                    
                    label.bind("<Button-1>", self.on_click_1)
                    label.bind("<Button-3>", self.on_click_2)
                    label.bind("<Enter>", self.onover)
                    label.bind("<Leave>", self.onleave)

                else:
                    label = Dia(self.BotFrame, text=day.day, bg="#D3D3D3", fg="#808080", font="Arial 11", width=10, height=2, border=8, date=day)
                    label.grid(row=i, column=j)

                    if day.month < month and day.year == self.ano_actual or day.month < month and day.year < self.ano_actual or day.month > month and day.year < self.ano_actual:
                        label.bind("<Button-1>", self.previousmonth)
                    else:
                        label.bind("<Button-1>", self.nextmonth)
                     
    def clearcalendar(self):
        for widget in self.BotFrame.winfo_children():
             widget.destroy()
        self.selected_label = {"label": None, "Color": None}

    def previousmonth(self, event):
        month = self.mes_actual - 1
        if month == 0:
            self.ano_actual -= 1
            month = 12
        if type (event.widget["text"]) == int:
            self.MesLabel.config(text=date(self.ano_actual, month, 1).strftime("%B %Y"))
            self.filldays(self.c.monthdatescalendar(self.ano_actual, month),month)
        else:
            self.filldays(self.c.monthdatescalendar(self.ano_actual, month), month)
            self.MesLabel.config(text=date(self.ano_actual, month, 1).strftime("%B %Y"))
        self.mes_actual = month
    def nextmonth(self, event):
        month = self.mes_actual + 1
        if month == 13:
            self.ano_actual += 1
            month = 1
        if type (event.widget["text"]) == int:
            self.MesLabel.config(text=date(self.ano_actual, month, 1).strftime("%B %Y"))
            self.filldays(self.c.monthdatescalendar(self.ano_actual, month),month)
        else:
            self.filldays(self.c.monthdatescalendar(self.ano_actual, month), month)
            self.MesLabel.config(text=date(self.ano_actual, month, 1).strftime("%B %Y"))
        self.mes_actual = month
        
    def on_click_1(self, event):
        label = event.widget
        if label["background"] == "#c3c3c3" and label == self.selected_label.get("label"):
            label.config(background=self.selected_label.get("Color"))
            self.selected_label["label"] = None
            self.selected_label["Color"] = None
        else:
            i = self.selected_label.get("label")
            if i != None:
                i.config(background=self.selected_label.get("Color"))
            self.selected_label["label"] = label
            self.selected_label["Color"] = label["background"]
            label.config(background="#c3c3c3")
            
    def on_click_2(self,event):
        label = event.widget
        Ventanita(label)
    def onover(self, event):
        label = event.widget
        if label["background"] == "#eeeeee":
          label.config(background="#c3c3c3")
    def onleave(self, event):
        label = event.widget
        if label != self.selected_label.get("label") and label["background"] == "#c3c3c3":
            label.config(background="#eeeeee")

root = Tk()
Calendario(root)
root.mainloop()