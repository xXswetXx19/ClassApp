
from tkinter import Button, Label, Entry, CENTER, messagebox
from Procesos.General import FillTw, updateList, CreateDirs
from Core.Database import run_query

class addMateriaView():
    def __init__(self, master) -> None:
        self.Add_win = master
        self.Add_win.resizable(width=False, height=False)
        self.Add_win.title = "Agregar Materia"
        self.Add_win.geometry("300x100")
        # self.Add_win.iconbitmap("Icono.ico")
        
        self.getLabels()
        self.getEntries()
        self.getButtons()
        
        
    def getButtons(self):
        self.addButton = Button(self.Add_win, text="Agregar", command=lambda: self.agg(self.CMateria.get()))
        self.addButton.place(anchor=CENTER, relx=0.5, rely=0.7)
    
    def getLabels(self):
        self.LMateria = Label(self.Add_win, text="Materia: ").place(anchor=CENTER, relx=0.2, rely=0.3)
        
    def getEntries(self):
        self.CMateria = Entry(self.Add_win, width=30)
        self.CMateria.place(anchor=CENTER, relx=0.6, rely=0.3)
        self.Add_win.bind("<Return>", lambda event: self.agg(self.CMateria.get()))
        
    def agg(self, Value):
        Value = Value.strip().capitalize()
        if not Value:
            return messagebox.showerror("Error", "No se puede agregar un campo vacio")
        
        if not Value.replace(" ", "").isalnum():  # Revisa que value solo tenga numeros y letras, nada de simbolos
            return messagebox.showerror("Error", "El nombre de la materia solo puede contener letras y numeros")
        
        if run_query(f"SELECT * FROM Materias WHERE Materia = ?", (Value,)).fetchone():
            return messagebox.showerror("Error", "La materia ya existe")
        run_query(f"INSERT INTO Materias VALUES(NULL, (?))", (Value,))
        self.Add_win.destroy()
        FillTw(self.Add_win)
        CreateDirs()
        updateList(self.Add_win)


