from Core.Core import Core
from tkinter import Tk

if __name__ == '__main__':
    root = Tk()
    App = Core.start(win=root)
    root.mainloop()