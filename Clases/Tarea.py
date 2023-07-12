import os
from Core.Database import Query

class Tarea:
    def __init__(self, id_tarea, materia, documento, numero, fechahora):
        self.query = Query()
        self.id_tarea = id_tarea
        self.materia = materia
        self.documento = documento
        self.numero = numero
        self.fechahora = fechahora
        self.fecha = self.fechahora.split(' ')[0]
        self.hora = self.fechahora.split(' ')[1]
        self.path = self.query.getHomeworksPath() 
        self.path = f"{self.path}\{self.documento}-{self.numero}.docx"
        
    def getFecha(self):
        return self.fecha
    
    def getHora(self):
        return self.hora
    
    def getMateria(self):
        return self.materia
    
    def getDocumento(self):
        return self.documento
    
    def getNumero(self):
        return self.numero
    
    def getFechaHora(self):
        return self.fechahora
    
    def getId(self):
        return self.id_tarea
    
    def delete(self):
        self.query.deleteHomework(self.id_tarea)
        os.remove(self.path)

    def open(self):
        os.startfile(self.path)

    def openLocation(self):
        os.startfile(self.path[:self.path.rfind('\\')])
   
    def convertPdf(self):
        pass
        # from Core.PdfConverter import convert
        # convert(self.path) 