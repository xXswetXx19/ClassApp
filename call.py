# from tkinter import *
# import tkcalendar

# # Crea la ventana Toplevel
# root = Tk()

# # Crea el widget Calendar
# calendar = tkcalendar.Calendar(root, font="Arial 14", selectmode="day", year=2022, month=12, day=1)
# calendar.pack(fill="both", expand=True)

# # Define la acción a realizar al hacer clic en un día del calendario
# def on_day_selected(event):
#     # Obtiene la fecha seleccionada
#     date = event.widget.selection_get()
#     print(f"Fecha seleccionada: {date}")

# # Asigna la función a la acción de hacer clic en un día del calendario
# calendar.bind("<1>", on_day_selected)


# root.mainloop()


import tkinter as tk
import calendar

# Crea la ventana principal
root = tk.Tk()

# Crea una matriz de botones para el calendario
buttons = [[None] * 7 for _ in range(6)]

# Crea el widget Calendar
c = calendar.Calendar(firstweekday=calendar.SUNDAY)
cal = c.monthdatescalendar(2022, 1)

# Crea los botones del calendario
for i, week in enumerate(cal):
    for j, day in enumerate(week):
        # Crea un botón para el día del mes
        # button = tk.Button(root, text=day.day, width=4,
        #                    command=lambda day=day: on_day_clicked(day))
        # button = tk.Label(root, anchor="center", text=day.day)
        button = tk.Label(root, text=day.day, bg="#eeeeee", fg="#444444", font="Helvetica 12", width=5, height=2)
        button.grid(row=i, column=j)
        buttons[i][j] = button

# Define la acción a realizar al hacer clic en un día del calendario
def on_day_clicked(day):
    # Obtiene la fecha seleccionada
    print(f"Fecha seleccionada: {day}")

# Muestra la ventana
root.mainloop()

# import tkinter as tk
# import calendar

# # Crea la ventana principal
# root = tk.Tk()

# # Crea una matriz de botones para el calendario
# buttons = [[None] * 7 for _ in range(6)]

# # Crea el widget Calendar
# c = calendar.Calendar(firstweekday=calendar.SUNDAY)
# cal = c.monthdatescalendar(2022, 1)

# # Crea los botones del calendario
# for i, week in enumerate(cal):
#     for j, day in enumerate(week):
#         # Si el día pertenece al mes de enero de 2022, crea un botón
#         if day.month == 1:
#             button = tk.Button(root, text=day.day, width=4,
#                                command=lambda day=day: on_day_clicked(day))
#             button.grid(row=i, column=j)
#             buttons[i][j] = button
#         # Si el día no pertenece al mes, deja el espacio en blanco
#         else:
#             tk.Label(root, text=" ", width=4).grid(row=i, column=j)

# # Define la acción a realizar al hacer clic en un día del calendario
# def on_day_clicked(day):
#     # Obtiene la fecha seleccionada
#     print(f"Fecha seleccionada: {day}")

# # Muestra la ventana
# root.mainloop()

# import tkinter as tk
# import calendar
# # Crea la ventana principal
# root = tk.Tk()
# # Crea una matriz de botones para el calendario
# buttons = [[None] * 7 for _ in range(6)]
# # Crea una variable para almacenar el mes seleccionado
# selected_month = tk.IntVar(value=1)

# # Crea una función para actualizar el calendario
# def update_calendar():
#     # Borra los botones del calendario anterior
#     for i in range(6):
#         for j in range(7):
#             button = buttons[i][j]
#             if button is not None:
#                 button.destroy()
#                 buttons[i][j] = None
#     # Crea el widget Calendar para el mes seleccionado
#     c = calendar.Calendar(firstweekday=calendar.SUNDAY)
#     cal = c.monthdatescalendar(2022, selected_month.get())
#     # Crea los botones del calendario
#     for i, week in enumerate(cal):
#         for j, day in enumerate(week):
#             # Si el día pertenece al mes seleccionado, crea un botón
#             if day.month == selected_month.get():
#                 button = tk.Button(root, text=day.day, width=4,
#                                    command=lambda day=day: on_day_clicked(day))
#                 button.grid(row=i+1, column=j)
#                 buttons[i][j] = button
#             # Si el día no pertenece al mes, deja el espacio en blanco
#             else:
#                 tk.Label(root, text=" ", width=4).grid(row=i+1, column=j)

# # Crea los botones para cambiar de mes
# prev_button = tk.Button(root, text="<", command=lambda: change_month(-1))
# prev_button.grid(row=0, column=0)
# next_button = tk.Button(root, text=">", command=lambda: change_month(1))
# next_button.grid(row=0, column=6)

# # Crea una etiqueta para mostrar el mes seleccionado
# month_label = tk.Label(root, textvariable=selected_month, width=4)
# month_label.grid(row=0, column=1, columnspan=4)

# def change_month(delta):
#     selected_month.set(selected_month.get() + delta)
#     update_calendar()

# def on_day_clicked(day):

#     print(f"Fecha seleccionada: {day}")

# # Muestra la ventana
# root.mainloop()