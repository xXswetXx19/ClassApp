from tkinter import *
import calendar


class Dia(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__Prioridad = 0
        self.__Descripcion = ["Hacer mates", "Dominar el mundo", "perriar hasta el piso"]
        
    def setPrioridad(self, prioridad):
        self.__Prioridad = prioridad
    def setDescripcion(self, descripcion):
        self.__Descripcion.append(descripcion)
    def getPrioridad(self):
        return self.__Prioridad
    def getDescripcion(self):
        return self.__Descripcion


class Ventanita:
    def __init__(self, label):
        win = Toplevel()
        win.title("Prioridad")
        win.geometry("400x200")
        win.resizable(0,0)
        color1 = "#eeeeee"
        color2 = "#F5F5DC"
        self.TopFrame = Frame(win, bg=color1)
        self.ButtonsFrame = Frame(win, bg="red")
        self.HomeworksFrame = Frame(self.TopFrame, bg=color2, bd=4, relief="ridge", width=400, height=150)
        # groove, sunken, flat 
        # ridge
        self.TopFrame.pack(expand= True, fill=BOTH, side=TOP)
        self.HomeworksFrame.grid(row=1, column=0, sticky='nsew')
        self.ButtonsFrame.pack(fill=BOTH, side=BOTTOM)

        self.TopFrame.grid_rowconfigure(1, minsize=130)
        self.TopFrame.grid_columnconfigure(0, minsize=400)


        LTareas = Label(self.TopFrame, text="Tareas", font=("Arial", 11, "bold"), background=color1)
        LTareas.grid(row=0, column=0, sticky=W)

        for i in range(len(label.getDescripcion())):
            Label(self.HomeworksFrame, text=label.getDescripcion()[i], font=("Arial", 11, "bold"), background=color2).grid(row=i+1, column=0, sticky=W)        
        
        Button(self.ButtonsFrame, text="Añadir Pendiente", font=("Arial", 11, "bold"), background="white", command=(), width=20).pack(side=LEFT)
        Button(self.ButtonsFrame, text="Eliminar Pendiente", font=("Arial", 11, "bold"), background="white", command=(), width=25).pack(side=RIGHT)
    #     # create a label for the priority
    #     Label(top, text="Prioridad", font=("Arial", 11, "bold"), background="white").pack()
    #     Label(top, text=label.getPrioridad(), font=("Arial", 11, "bold"), background="white").pack()
    #     # create a label for the description
    #     Label(top, text="Descripción", font=("Arial", 11, "bold"), background="white").pack()
    #     for i in label.getDescripcion():
    #         Label(top, text=i, font=("Arial", 11, "bold"), background="white").pack()
    #     # create a button for add a new description
    #     Button(top, text="Añadir descripción", font=("Arial", 11, "bold"), background="white", command=lambda: self.addDescripcion(label)).pack()
    #     # create a button for add a new priority
    #     Button(top, text="Añadir prioridad", font=("Arial", 11, "bold"), background="white", command=lambda: self.addPrioridad(label)).pack()
    #     # create a button for delete the priority
    #     Button(top, text="Eliminar prioridad", font=("Arial", 11, "bold"), background="white", command=lambda: self.deletePrioridad(label)).pack()
    #     # create a button for delete the description
    #     Button(top, text="Eliminar descripción", font=("Arial", 11, "bold"), background="white", command=lambda: self.deleteDescripcion(label)).pack()
    # def addDescripcion(self, label):
    #     top = Toplevel()
    #     top.title("Añadir descripción")
    #     top.geometry("300x300")
    #     top.resizable(0,0)
    #     top.config(cursor="hand2")
    #     top.config(bd=15)
    #     top.config(relief="groove")
        
    #     Label(top, text="Descripción", font=("Arial", 11, "bold"), background="white").pack()
    #     Entry(top, textvariable=StringVar(), font=("Arial", 11, "bold"), background="white").pack()
    #     Button(top, text="Añadir", font=("Arial", 11, "bold"), background="white", command=lambda: self.addDescripcion2(label)).pack()
    # def addDescripcion2(self, label):
    #     label.addDescripcion("Hola")
    #     print(label.getDescripcion())
    # def addPrioridad(self, label):
    #     top = Toplevel()
    #     top.title("Añadir prioridad")
    #     top.geometry("300x300")
    #     top.resizable(0,0)
    #     top.config(cursor="hand2")
        
    #     Label(top, text="Prioridad", font=("Arial", 11, "bold"), background="white").pack()
    #     Entry(top, textvariable=StringVar(), font=("Arial", 11, "bold"), background="white").pack()
    #     Button(top, text="Añadir", font=("Arial", 11, "bold"), background="white", command=lambda: self.addPrioridad2(label)).pack()
    # def addPrioridad2(self, label):
    #     label.addPrioridad("Hola")
    #     print(label.getPrioridad())
    

class Calendario:
    def __init__ (self, window):
# Crea la ventana principal y el calendario
        self.window = window
        self.window.geometry("755x375")
        self.window.title("Calendario")
        self.window.resizable(0,0)
        self.TopFrame = Frame(self.window,background="#006064", height=50)
        self.CenterFrame = Frame(self.window, background="green", height=30)
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
                    label = Dia(self.BotFrame, text=day.day, bg="#eeeeee", font="Arial 11", width=10, height=2, border=8)
                    label.grid(row=i, column=j)
                    label.bind("<Button-1>", self.on_click_1)
                    label.bind("<Button-3>", self.on_click_2)
                    label.bind("<Enter>", self.onover)
                    label.bind("<Leave>", self.onleave)

                else:
                    label = Dia(self.BotFrame, text=day.day, bg="#D3D3D3", fg="#808080", font="Arial 11", width=10, height=2, border=8)
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