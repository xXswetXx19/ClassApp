from Core.Database import *
from tkinter import Tk
from views.App import APP

class Core:
    def __init__(self):
        self.master = Tk()

    def start(self):
        self.startDatabase()
        self.App = APP(self.master)
        self.master.mainloop()

    def startDatabase(self):
        createDB()




# class VerPendientes:
#     def __init__(self):
#         self.win = Toplevel()
#         self.win.title("Tareas")
#         self.win.geometry("300x400")
#         self.win.resizable(0,0)
#         color1 = "#eeeeee"
#         self.HomeworksFrame = Frame(self.win, bg=color1, bd=4, relief="ridge", width=300, height=400)
#         self.HomeworksFrame.grid(row=1, column=0, sticky=NSEW)
#         self.listcolors = ["#ffffff", "#eeeeee", "#dddddd", "#cccccc", "#bbbbbb", "#aaaaaa", "#999999", "#888888", "#777777", "#666666", "#555555", "#444444", "#333333", "#222222", "#111111", "#000000"]
#         self.FillPending()
#     def FillPending(self):
#         for i, color in enumerate(self.listcolors):
#             Label(self.HomeworksFrame, text = "Hola", bg = color).grid(row = i, column = 0)

        