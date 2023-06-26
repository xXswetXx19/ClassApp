import os
from Core.Database import Query 
from Procesos.Principales import getPath
from tkinter import *
from tkinter import messagebox
import datetime as datetime
from datetime import date, datetime
from docxtpl import DocxTemplate
import subprocess
from Procesos.Principales import getPath, getMaterias, CreateDirs
import docx2pdf


Plantilla_Path = os.path.join("Archivos", "plantilla.docx")

db = Query()


def CreateTarea(self):
    Path = getPath() 
    try:
        Materia = self.tree.item(self.tree.selection())["values"][0]
    except:
        return messagebox.showerror("Error", "Seleccione una materia")
    DatosConfig = db.run_query("SELECT * FROM Configuracion").fetchone()
    if not DatosConfig:
        return messagebox.showerror("Error", "Agregue sus datos en la configuracion para crear una tarea")
    Id, Nombres, Apellidos, Paralelo, Ruta = DatosConfig
    if not os.path.exists(f"{Path}\Tareas\{Materia}"):
        CreateDirs(self)
    Fecha = date.strftime(datetime.now(), "%d.%m.%Y")
    Nums = db.run_query(f"SELECT cantidad FROM Cantidad WHERE Fecha = ?", (Fecha,))
    Result = list(Nums)
    if len(Result) > 0:
        Num = int(Result[0][0]) + 1
        db.run_query(f"UPDATE Cantidad SET cantidad = ? WHERE Fecha = ?", (Num, Fecha))
    else:
        db.run_query(f"INSERT INTO Cantidad VALUES (NULL, ?, ?)", (Fecha, 1))
        Num = 1
    doc = DocxTemplate(Plantilla_Path)
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
    db.run_query(f"DELETE FROM Materias WHERE Id = ?", (Id,))
    FillTw(self)


def clearviewTw(self):
    records = self.view_tree.get_children()
    for element in records:
        self.view_tree.delete(element)

def getHomeworks(self):
    Path = getPath()
    clearviewTw(self)
    if os.path.exists(f"{Path}\Tareas"):
        Classdirs = os.listdir(f"{Path}\Tareas")
        for ClassDir in Classdirs:
            if os.path.isdir(f"{Path}\Tareas\{ClassDir}"):
                Homeworks = os.scandir(f"{Path}\Tareas\{ClassDir}")
                for Homework in Homeworks:
                    timestamp = os.path.getctime(Homework.path)
                    Date = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y')
                    Hour = datetime.fromtimestamp(timestamp).strftime('%H:%M')
                    Num = Homework.name.split("-")[2].split(".")[0]
                    Doctype = Homework.name.split("-")[2].split(".")[1].capitalize()
                    if Doctype == "Docx":
                        Doctype = "Word"
                    self.view_tree.insert('', 0, text = Homework, values = (ClassDir, Doctype, Num, Date, Hour), tags = ("Tareas"))
def DeleteHomework(self):
    Path = getPath()
    try:
        Homework = self.view_tree.item(self.view_tree.selection())['text'].split("'")[1]
        Class = self.view_tree.item(self.view_tree.selection())['values'][0]
    except:
        return messagebox.showerror("Error", "No se ha seleccionado ninguna tarea")
    ask = messagebox.askyesno("¿Esta seguro de eliminar la tarea?", "¿Esta seguro de eliminar la tarea?")
    if ask:
        os.remove(f"{Path}\Tareas\{Class}\{Homework}")
        self.view_tree.delete(self.view_tree.selection())
    else:      return
def OpenHomework(self):
    Path = getPath()
    try:
        Homework = self.view_tree.item(self.view_tree.selection())['text'].split("'")[1]
        Class = self.view_tree.item(self.view_tree.selection())['values'][0]
    except:
        return messagebox.showerror("Error", "No se ha seleccionado ninguna tarea")
    os.startfile(f"{Path}\Tareas\{Class}\{Homework}")

def OpenPath(self):
    Path = getPath()
    try:
        Homework = self.view_tree.item(self.view_tree.selection())['text'].split("'")[1]
        Class = self.view_tree.item(self.view_tree.selection())['values'][0]
    except:
        return messagebox.showerror("Error", "No se ha seleccionado ninguna tarea")
    HomeWorkPath = f"{Path}\\Tareas\\{Class}\\{Homework}".replace("/", "\\") 
    subprocess.Popen(r'explorer /select,"{FilePath}"'.format(FilePath=HomeWorkPath))

def DoctoPdf(self):
    Path = getPath()
    try:
        Homework = self.view_tree.item(self.view_tree.selection())['text'].split("'")[1]
        Class = self.view_tree.item(self.view_tree.selection())['values'][0]
    except:
        return messagebox.showerror("Error", "No se ha seleccionado ninguna tarea")
    DocPath = f"{Path}\Tareas\{Class}\{Homework}"
    
    if not DocPath.endswith(".docx"):
        return messagebox.showerror("Error", "El archivo seleccionado no es un documento de word")
    docx2pdf.convert(DocPath)
    os.startfile(DocPath.replace(".docx", ".pdf"))