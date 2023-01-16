class Tarea:
    def __init__(self, Materia, Fecha, Descripcion, Prioridad):
        self.Materia = Materia     
        self.Descripcion = Descripcion
        self.Prioridad = Prioridad
        self.Fecha = Fecha
    def __str__(self):
        return f"{self.Materia} + {self.Fecha} + {self.Prioridad}"

class TareaGrupal(Tarea):
    def __init__(self, Materia, Fecha, Descripcion, Integrantes):
        super().__init__(Materia = Materia, Fecha = Fecha, Descripcion = Descripcion)
        self.Integrantes = Integrantes
