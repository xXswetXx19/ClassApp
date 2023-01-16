
import os
from Core.Database import run_query
from tkinter import *
from tkinter import messagebox
import datetime as datetime
from datetime import date
from docxtpl import DocxTemplate


def FillTw(self):
    self.clearTw()
    db_rows = run_query('SELECT * FROM Materias')
    for row in db_rows:
        Materia = (row[1],)
        self.tree.insert('', 0, text = row[0], values = Materia, tags=('Materias'))
def clearTw(self):
    records = self.tree.get_children()
    for element in records:
        self.tree.delete(element)

def CreateTarea(self):
    try:
        Materia = self.tree.item(self.tree.selection())["values"][0]
    except:
        return messagebox.showerror("Error", "Seleccione una materia")
    DatosConfig = run_query("SELECT * FROM Configuracion").fetchone()
    if not DatosConfig:
        return messagebox.showerror(
            "Error", "Agregue sus datos en la configuracion para crear una tarea"
        )
    Id, Nombres, Apellidos, Paralelo, Ruta = DatosConfig
    if not os.path.exists(f"{Path}\Tareas\{Materia}"):
        self.CreateDirs()
    Fecha = date.strftime(date.now(), "%d.%m.%Y")
    Nums = run_query(f"SELECT cantidad FROM Cantidad WHERE Fecha = ?", (Fecha,))
    Result = list(Nums)
    if len(Result) > 0:
        Num = int(Result[0][0]) + 1
        run_query(f"UPDATE Cantidad SET cantidad = ? WHERE Fecha = ?", (Num, Fecha))
    else:
        run_query(f"INSERT INTO Cantidad VALUES (NULL, ?, ?)", (Fecha, 1))
        Num = 1
    doc = DocxTemplate("plantilla.docx")
    doc.render(
        {
            "MATERIA": Materia,
            "FECHA": Fecha.replace(".", "/"),
            "NOMBRES": Nombres,
            "APELLIDOS": Apellidos,
            "PARALELO": Paralelo,
        }
    )
    Document_Path = rf"{Path}/Tareas/{Materia}/Tarea-{Fecha}-{Num}.docx"
    doc.save(Document_Path)
    os.startfile(Document_Path)
    try:
        self.view_win_functions.getHomeworks()
    except:
        pass


def removeMateria(self):
    Id = self.tree.item(self.tree.selection())["text"]
    if not Id:
        return messagebox.showerror("Error", "Seleccione una materia")
    run_query(f"DELETE FROM Materias WHERE Id = ?", (Id,))
    self.FillTw()

def addMateria(self):
    if any(isinstance(x, Toplevel) for x in self.master.winfo_children()):
        if self.Add_win.winfo_exists() if self.Add_win.winfo_exists() else False:
            messagebox.showerror("Error", "Ya hay una ventana")
            return self.Add_win.lift()
    self.Add_win = Toplevel()
    self.Add_win.resizable(width=False, height=False)
    self.Add_win.title = "Agregar Materia"
    self.Add_win.geometry("300x100")
    self.Add_win.iconbitmap("Icono.ico")

    def agg(Value):
        Value = Value.strip().capitalize()
        if not Value:
            return messagebox.showerror(
                "Error", "No se puede agregar un campo vacio"
            )
        if not Value.replace(" ", "").isalnum():  # Revisa que value solo tenga numeros y letras, nada de simbolos
            return messagebox.showerror("Error", "El nombre de la materia solo puede contener letras y numeros")
        if run_query(f"SELECT * FROM Materias WHERE Materia = ?", (Value,)).fetchone():
            return messagebox.showerror("Error", "La materia ya existe")
        run_query(f"INSERT INTO Materias VALUES(NULL, (?))", (Value,))
        self.Add_win.destroy()
        self.FillTw()
        self.CreateDirs()
        self.__updateList()

    LMateria = Label(self.Add_win, text="Materia: ").place(anchor=CENTER, relx=0.2, rely=0.3)
    CMateria = Entry(self.Add_win, width=30)
    CMateria.place(anchor=CENTER, relx=0.6, rely=0.3)
    Boton = Button(
    self.Add_win, text="Agregar", command=lambda: agg(CMateria.get())).place(anchor=CENTER, relx=0.5, rely=0.7)
    self.Add_win.bind("<Return>", lambda event: agg(CMateria.get()))




