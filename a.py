# create a calendar using tk calendar
import tkcalendar
import tkinter as tk
# create a tkinter window
root = tk.Tk()

root.geometry("400x400")
root.title("CALENDARIO")
root.configure(background="white")
root.resizable(0,0)
root.config(cursor="hand2")
root.config(bd=15)
root.config(relief="groove")
root.config(bg="white")
# create a calendar
calendar = tkcalendar.Calendar(root, selectmode="day", year=2021, month=12, day=31)
root.mainloop()