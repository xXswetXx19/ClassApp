import os
from Core.Database import Query
from tkinter import messagebox
from datetime import date, datetime
from docxtpl import DocxTemplate
import subprocess
import docx2pdf

class HomeworkProcess():
    def __init__(self, CustomTreeview, HomeWorksWin = None) -> None:
        self.database = "database.db"
        self.query = Query()
        self.treeview = CustomTreeview
        self.Plantilla_Path = os.path.join("Archivos", "plantilla.docx")
        self.HomeworksPath = self.query.getHomeworksPath()
        self.HomeWorksWin = HomeWorksWin
        
    def CreateTarea(self) -> None:
        Materia = self.treeview.get_tree_selection()["values"][0]
        if not Materia:
            return messagebox.showerror("Error", "Seleccione una materia")
        
        DatosConfig = self.query.getConfigData()
        if not DatosConfig:
            return messagebox.showerror("Error", "Agregue sus datos en la configuracion para crear una tarea")
        
        Id, Nombres, Apellidos, Paralelo, Ruta = DatosConfig
        
        if not os.path.exists(f"{self.HomeworksPath}\Tareas\{Materia}"):
            self.CreateDirs()            
            
        Fecha = date.strftime(datetime.now(), "%d.%m.%Y")
        
        TareasHoy = self.query.getHomeworks(Fecha)

        Num = int(len(TareasHoy)) + 1
        self.query.createHomework(Fecha, Materia)

        doc = DocxTemplate(self.Plantilla_Path)
        doc.render(
            {
                "MATERIA": Materia,
                "FECHA": Fecha.replace(".", "/"),
                "NOMBRES": Nombres,
                "APELLIDOS": Apellidos,
                "PARALELO": Paralelo,
            }
        )
        
        os.mkdir(rf"{self.HomeworksPath}/Tareas/{Materia}/{Fecha}")
        
        Document_Path = rf"{self.HomeworksPath}/Tareas/{Materia}/{Fecha}/Tarea-{Fecha}-{Num}.docx"
        
        doc.save(Document_Path)
        
        os.startfile(Document_Path)
        
        if self.HomeWorksWin:
            self.HomeWorksWin.getHomeworks()


    def removeMateria(self):
        Materia = self.treeview.get_tree_selection()["values"][0]
        if not Materia:
            return messagebox.showerror("Error", "Seleccione una materia")
        self.query.deleteMateria(Materia)

        Materias = self.query.getMaterias()
        self.treeview.update_completion_list(Materias)


    # HomeWorkView Functions


    def clearviewTw(self):
        records = self.HomeWorksWin.treeview.get_children()
        for element in records:
            self.HomeWorksWin.treeview.delete(element)

    def getHomeworks(self):
        Path = self.query.getHomeworksPath()
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
                        self.HomeWorksWin.treeview.insert('', 0, text = Homework, values = (ClassDir, Doctype, Num, Date, Hour), tags = ("Tareas"))
    def DeleteHomework(self):
        try:
            Homework = self.HomeWorksWin.treeview.item(self.HomeWorksWin.treeview.selection())['text'].split("'")[1]
            Class = self.HomeWorksWin.treeview.item(self.HomeWorksWin.treeview.selection())['values'][0]
        except:
            return messagebox.showerror("Error", "No se ha seleccionado ninguna tarea")
        ask = messagebox.askyesno("¿Esta seguro de eliminar la tarea?", "¿Esta seguro de eliminar la tarea?")
        if ask:
            os.remove(f"{self.HomeworksPath}\Tareas\{Class}\{Homework}")
            self.HomeWorksWin.treeview.delete(self.HomeWorksWin.treeview.selection())
        else:      return
    def OpenHomework(self):
        try:
            Homework = self.HomeWorksWin.treeview.item(self.HomeWorksWin.treeview.selection())['text'].split("'")[1]
            Class = self.HomeWorksWin.treeview.item(self.HomeWorksWin.treeview.selection())['values'][0]
        except:
            return messagebox.showerror("Error", "No se ha seleccionado ninguna tarea")
        os.startfile(f"{self.HomeworksPath}\Tareas\{Class}\{Homework}")

    def OpenPath(self):
        try:
            Homework = self.HomeWorksWin.treeview.item(self.HomeWorksWin.treeview.selection())['text'].split("'")[1]
            Class = self.HomeWorksWin.treeview.item(self.HomeWorksWin.treeview.selection())['values'][0]
        except:
            return messagebox.showerror("Error", "No se ha seleccionado ninguna tarea")
        HomeWorkPath = f"{self.HomeworksPath}\\Tareas\\{Class}\\{Homework}".replace("/", "\\") 
        subprocess.Popen(r'explorer /select,"{FilePath}"'.format(FilePath=HomeWorkPath))

    def DoctoPdf(self):
        try:
            Homework = self.HomeWorksWin.treeview.item(self.HomeWorksWin.treeview.selection())['text'].split("'")[1]
            Class = self.HomeWorksWin.treeview.item(self.HomeWorksWin.treeview.selection())['values'][0]
        except:
            return messagebox.showerror("Error", "No se ha seleccionado ninguna tarea")
        DocPath = f"{self.HomeworksPath}\Tareas\{Class}\{Homework}"
        
        if not DocPath.endswith(".docx"):
            return messagebox.showerror("Error", "El archivo seleccionado no es un documento de word")
        docx2pdf.convert(DocPath)
        os.startfile(DocPath.replace(".docx", ".pdf"))
            
    def CreateDirs(self):
        Materias = getMaterias()
        if not os.path.exists(f"{self.HomeworksPath}\Tareas"):
            os.mkdir(f"{self.HomeworksPath}\Tareas")
        for Materia in Materias:
            if not os.path.exists(f"{self.HomeworksPath}\Tareas\{Materia}"):
                os.mkdir(f"{self.HomeworksPath}\Tareas\{Materia}")


