from tkinter import Label 
from Core.Database import search_DayData

class Dia(Label):
    def __init__(self, *args, **kwargs):
        date = kwargs.pop('date', None)
        super().__init__(*args,**kwargs)
        self.Dia = date.day
        self.Mes = date.month
        self.Año = date.year
        self.__Notas = []
        
    def addNota(self, descripcion):
        self.__Notas.append(descripcion)
    def getDescripcion(self):
        self.__Notas.sort(key=lambda x: ["Baja", "Media", "Alta","Urgente"].index(x[1]), reverse=True)
        return self.__Notas
    def getday(self):
        return self.Dia
    def getmonth(self):
        return self.Mes
    def getyear(self):
        return self.Año
    def updateDayData(self):
        DayData = search_DayData(dia=self.Dia, mes=self.Mes, año=self.Año)
        self.__Notas = []
        if DayData:
            for Data in DayData:
                Id, dia, mes, año, descripcion, prioridad = Data
                self.__Notas.append([Id, prioridad, descripcion])