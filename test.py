from Clases.Tarea import Tarea
from Core.Database import Query

query = Query()

tarea = query.getHomeworksList()[0]

tarea = Tarea(tarea[0], tarea[1], tarea[2], tarea[3], tarea[4])