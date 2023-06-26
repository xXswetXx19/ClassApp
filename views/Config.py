from tkinter import Button, Entry, Label, StringVar, W, messagebox, filedialog, DISABLED, CENTER
from Core.Database import Query
db = Query()


from Procesos.Principales import getPath, getMaterias
class ConfigWin:
    def __init__(self, toplevel, master):
        self.Config_win = toplevel
        self.Config_win.resizable(width=False, height=False)
        self.Config_win.title = 'Configuración'
        self.Config_win.geometry('500x150')
        self.Config_win.iconbitmap("Archivos/Icono.ico")

        Path = getPath()
        self.ConfigData = db.run_query('SELECT * FROM Configuracion').fetchone()
        Datos = ["Nombres:", "Apellidos:", "Paralelo:", "Ruta:"]
        
        for i in Datos:
            Label(self.Config_win, text = i).place(anchor = W, relx = .1, rely = .1 + (Datos.index(i) * .2))
            if self.ConfigData:
                Entry(self.Config_win, textvariable = StringVar(self.Config_win, value= self.ConfigData[Datos.index(i)+1]), width=50).place(anchor = CENTER, relx = .6, rely = .1 + (Datos.index(i) * .2))
            else:
                Entry(self.Config_win, width=50).place(anchor = CENTER, relx = .6, rely = .1 + (Datos.index(i) * .2))
        
        self.Entries = [i for i in self.Config_win.children.values() if type(i) == Entry]
        self.RutaEntry = self.Entries[3]
        self.RutaEntry.config(state = DISABLED)
        # getPath()
        self.RutaEntry['textvariable'] = StringVar(self.Config_win, value = Path)
        self.RutaEntry.bind("<Button-1>", lambda x: self.browsedir())
        
        Boton1 = Button(self.Config_win, text = 'Guardar', command = lambda: self.agg())
        Boton1.place(anchor = CENTER, relx = .5, rely = .9)
        self.Config_win.bind('<Return>', lambda event: self.agg())
    def agg(self):
        data = [i.get() for i in self.Entries]
        Nombres, Apellidos, Paralelo, Ruta = data
        if not Nombres or not Apellidos or not Paralelo:
            return messagebox.showerror("Error", "Verifique que los campos de Nombres, Apellidos y Paralelo no esten vacios")
        if self.ConfigData:
            Id = self.ConfigData[0]
            query = f'UPDATE Configuracion SET Nombres = ?, Apellidos = ?, Paralelo = ?, Ruta = ? WHERE Id = ?'
            db.run_query(query, (Nombres.strip(), Apellidos.strip(), Paralelo.strip(), Ruta, Id))
            self.Config_win.destroy()
        else: 
            query = f'INSERT INTO Configuracion VALUES(NULL, ?, ?, ?, ?)'
            db.run_query(query, (Nombres, Apellidos, Paralelo, Ruta))
            self.Config_win.destroy()
        # getPath()
    def browsedir(self):
        Dirname = filedialog.askdirectory()
        if Dirname:
            self.RutaEntry["textvariable"] = StringVar(self.Config_win, value = Dirname)  