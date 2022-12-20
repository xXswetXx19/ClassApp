from tkinter import *
from tkinter import ttk
import calendar


class Dia(Label):
    def __init__(self, *args, **kwargs):
        date = kwargs.pop('date', None)
        super().__init__(*args,**kwargs)

        self.Dia = date.day
        self.Mes = date.month
        self.Año = date.year

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
    def getFecha(self):
        return self.Fecha

class Ventanita:
    def __init__(self, widgetday):
        win = Toplevel()
        win.title("Tareas")
        win.geometry("400x200")
        # win.resizable(0,0)
        color1 = "#eeeeee"
        color2 = "#F5F5DC"
        self.TopFrame = Frame(win, bg=color1)
        self.ButtonsFrame = Frame(win, bg="red")
        self.HomeworksFrame = Frame(self.TopFrame, bg=color1, bd=4, relief="ridge", width=400, height=150)
    
        self.TopFrame.pack(expand= True, fill=BOTH, side=TOP)
        self.HomeworksFrame.grid(row=1, column=0, sticky='nsew')
        self.ButtonsFrame.pack(fill=BOTH, side=BOTTOM)

        self.TopFrame.grid_rowconfigure(1, minsize=150)
        self.TopFrame.grid_columnconfigure(0, minsize=400)

        LTareas = Label(self.TopFrame, text=widgetday.getday(), font=("Arial", 11, "bold"), background=color1)
        LTareas.grid(row=0, column=0, sticky=W)
        
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
        for Prioridad, Nota in widgetday.getDescripcion():
            row = self.view_tree.insert("", "end", text=Nota, values=Prioridad)
            if Prioridad == "Baja":
                self.view_tree.item(row, tags="Baja")
            elif Prioridad == "Media":
                self.view_tree.item(row, tags="Media")
            elif Prioridad == "Alta":
                self.view_tree.item(row, tags="Alta")
            elif Prioridad == "Urgente":
                self.view_tree.item(row, tags="Urgente")
            
        Button(self.ButtonsFrame, text="Añadir Pendiente", font=("Arial", 11, "bold"), background=color1, command=(), width=20).pack(side=LEFT)
        Button(self.ButtonsFrame, text="Eliminar Pendiente", font=("Arial", 11, "bold"), background=color1, command=(), width=25).pack(side=RIGHT)


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
        self.CenterFrame.pack(expand= True, fill = BOTH, side=TOP)
        self.BotFrame.pack(fill=BOTH, side=BOTTOM)
        
        # Crea el widget Calendar
        c = calendar.Calendar(firstweekday=calendar.MONDAY)
        cal = c.monthdatescalendar(2022, 12)

        # Top Frame
        self.butt1 = Label(self.TopFrame, text = "<",width= 5, height=3, font=(10), background= "#006064", foreground= "white")
        self.butt1.pack(side = LEFT, anchor=CENTER)
        self.butt2 = Label(self.TopFrame, text = ">", width= 5, height=3, font=(10), background= "#006064", foreground= "white")
        self.butt2.pack(side = RIGHT, anchor=CENTER)
        self.MesLabel = Label(self.TopFrame, text= "Diciembre",background="#006064",foreground= "#FFFFFF", font=("Arial Black", 21)).pack(anchor=CENTER, expand=True)

        self.butt1.bind("<Enter>", lambda event: self.butt1.config(background="#004d4d"))
        self.butt1.bind("<Leave>", lambda event: self.butt1.config(background="#006064"))
        self.butt2.bind("<Enter>", lambda event: self.butt2.config(background="#004d4d"))
        self.butt2.bind("<Leave>", lambda event: self.butt2.config(background="#006064"))

        # Center Frame
        Dias = ("Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo")
        for i, dia in enumerate(Dias):
            Label(self.CenterFrame,background="#006064",text=dia, font=("Arial", 11, "bold"), foreground= "#FFFFFF", width=10, height=2, border= 8).grid(row=0, column=i)
        
        # Bot Frame
        for i, week in enumerate(cal):
            for j, day in enumerate(week):
                if day.month == 12: # Si el día pertenece al mes de enero de 2022, crea un botón
                    label = Dia(self.BotFrame, text=day.day, bg="#eeeeee", font="Arial 11", width=10, height=2, border=8, date=day)
                    label.grid(row=i, column=j)
                    label.bind("<Button-1>", self.on_click_1)
                    label.bind("<Button-3>", self.on_click_2)
                    label.bind("<Enter>", self.onover)
                    label.bind("<Leave>", self.onleave)

                else:
                    label = Dia(self.BotFrame, text=day.day, bg="#D3D3D3", fg="#808080", font="Arial 11", width=10, height=2, border=8, date=day)
                    label.grid(row=i, column=j)
        
        self.selected_label = []
    def on_click_1(self, event):
        label = event.widget
        if label["background"] == "#c3c3c3" and label in self.selected_label:
            label.config(background="#eeeeee")
        else:
            for i in self.selected_label:
                i.config(background="#eeeeee")
                self.selected_label.pop()
            label.config(background="#c3c3c3")
            self.selected_label.append(label)
    def on_click_2(self,event):
        label = event.widget
        Ventanita(label)
    def onover(self, event):
        label = event.widget
        label.config(background="#c3c3c3")
    def onleave(self, event):
        label = event.widget
        if label not in self.selected_label:
            label.config(background="#eeeeee")

root = Tk()
Calendario(root)
root.mainloop()