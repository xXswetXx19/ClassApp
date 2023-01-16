import os
from datetime import datetime
from datetime import date
from tkinter import messagebox
import subprocess

def getHomeworks(self):
    self.clearviewTw()
    if os.path.exists(f"{Path}\Tareas"):
        Classdirs = os.listdir(f"{Path}\Tareas")
        for ClassDir in Classdirs:
            if os.path.isdir(f"{Path}\Tareas\{ClassDir}"):
                Homeworks = os.scandir(f"{Path}\Tareas\{ClassDir}")
                for Homework in Homeworks:
                    timestamp = os.path.getctime(Homework.path)
                    Date = date.fromtimestamp(timestamp).strftime('%d/%m/%Y')
                    Hour = date.fromtimestamp(timestamp).strftime('%H:%M')
                    Num = Homework.name.split("-")[2].split(".")[0]
                    self.view_tree.insert('', 0, text = Homework, values = (ClassDir, Num, Date, Hour), tags = ("Tareas"))
def DeleteHomework(self):
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
    try:
        Homework = self.view_tree.item(self.view_tree.selection())['text'].split("'")[1]
        Class = self.view_tree.item(self.view_tree.selection())['values'][0]
    except:
            os.startfile(f"{Path}\Tareas\{Class}\{Homework}")
def OpenPath(self):
    try:
        Homework = self.view_tree.item(self.view_tree.selection())['text'].split("'")[1]
        Class = self.view_tree.item(self.view_tree.selection())['values'][0]
    except:
        return messagebox.showerror("Error", "No se ha seleccionado ninguna tarea")
    HomeWorkPath = f"{Path}\\Tareas\\{Class}\\{Homework}".replace("/", "\\") 
    subprocess.Popen(r'explorer /select,"{FilePath}"'.format(FilePath=HomeWorkPath))
