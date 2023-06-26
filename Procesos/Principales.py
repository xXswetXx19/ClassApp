from Core.Database import Query
import os
db = Query()
def getPath():
    Path = db.run_query("SELECT Ruta FROM Configuracion").fetchone()
    Path = Path[0] if Path else os.getcwd()
    return Path


def getMaterias():
    Materias = db.run_query("SELECT Materia FROM Materias").fetchall()
    Materias = [i[0] for i in Materias]
    return Materias


def CreateDirs():
    Path = getPath()
    Materias = getMaterias()
    if not os.path.exists(f"{Path}\Tareas"):
        os.mkdir(f"{Path}\Tareas")
    for Materia in Materias:
        if not os.path.exists(f"{Path}\Tareas\{Materia}"):
            os.mkdir(f"{Path}\Tareas\{Materia}")




