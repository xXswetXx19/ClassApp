from tkinter import *
import calendar

class Calendario:
    def __init__ (self, window):
# Crea la ventana principal y el calendario
        self.window = window
        self.window.geometry("545x285")
        self.TopFrame = Frame(self.window,background="#D3D3D3", height=50)
        self.CenterFrame = Frame(self.window, background="green", height=30)
        self.BotFrame = Frame(self.window,background="red", height=205)
        
        self.TopFrame.pack(fill = BOTH, side=TOP)
        self.CenterFrame.pack(expand= True, fill = BOTH, side=TOP)
        self.BotFrame.pack(fill=BOTH, side=BOTTOM)
        # Crea el widget Calendar
        c = calendar.Calendar(firstweekday=calendar.MONDAY)
        cal = c.monthdatescalendar(2022, 12)
        Dias = ("Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo")
        for i, dia in enumerate(Dias):
            # lb = Label(self.CenterFrame, text=dia).pack(side="left", fill=BOTH, expand=True)
            lv = Label(self.CenterFrame,background="#D3D3D3",text=dia, font="Arial 11", width=8, height=2).grid(row=0, column=i)
            # .pack(side="left", fill= BOTH)
        
        self.Button1 = Button(self.TopFrame, text="<").pack(side = LEFT, anchor=CENTER)
        self.Button1 = Button(self.TopFrame,text=">").pack(side = RIGHT, anchor=CENTER)
        self.MesLabel = Label(self.TopFrame, text= "Diciembre",background="#D3D3D3", font=("Arial Black", 21)).pack(anchor=CENTER, expand=True)

            
        for i, week in enumerate(cal):
            for j, day in enumerate(week):
        # Si el día pertenece al mes de enero de 2022, crea un botón
                if day.month == 12:
                    label = Label(self.BotFrame, text=day.day, bg="#eeeeee", fg="#444444", font="Arial 11", width=8, height=2)
                    label.grid(row=i, column=j)
                    label.bind("<Button-1>", self.on_click_1)
                    label.bind("<Button-3>", self.on_click_2)
                else:
                    label = Label(self.BotFrame, text=day.day, bg="#D3D3D3", fg="#444444", font="Arial 11", width=8, height=2)
                    label.grid(row=i, column=j)


  
                    
                    
        
        self.selected_label = []
    # Función que se ejecuta cuando se hace clic en una etiqueta del calendario
    def on_click_1(self, event):
        label = event.widget
        if label["background"] == "red":
            label.config(background="#eeeeee")
        else:
            for i in self.selected_label:
                i.config(background="#eeeeee")
                self.selected_label.pop()
            print(self.selected_label)
            label.config(background="red")
            self.selected_label.append(label)
    def on_click_2(self,event):
        label = event.widget
        label.config(foreground = "blue")
root = Tk()
Calendario(root)
root.mainloop()