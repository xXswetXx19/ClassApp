
from tkinter import Button, Label, Entry, CENTER, messagebox
from Procesos.General import CreateDirs
from Core.Database import Query
class addMateriaView():
    def __init__(self, toplevel, master) -> None:
        self.master = master
        self.Add_win = toplevel
        self.Add_win.resizable(width=False, height=False)
        self.Add_win.title = "Agregar Materia"
        self.Add_win.geometry("300x100")
        # self.Add_win.iconbitmap("Icono.ico")
        self.db = Query()
                
        self.getLabels()
        self.getEntries()
        self.getButtons()
        
        
    def getButtons(self):
        self.button = Button(self.Add_win, text="Agregar", command=lambda: self.agg(self.CMateria.get()))
        self.button.place(anchor=CENTER, relx=0.5, rely=0.7)
    
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
        
        if self.db.run_query(f"SELECT * FROM Materias WHERE Materia = ?", (Value,)).fetchone():
            return messagebox.showerror("Error", "La materia ya existe")
        self.db.run_query(f"INSERT INTO Materias VALUES(NULL, (?))", (Value,))
        self.Add_win.destroy()
        materias = self.db.getMaterias()
        self.master.entry.update_completion_list(materias)         
        CreateDirs()



