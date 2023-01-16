import pandas as pd
from datetime import datetime
import time
import sqlite3 as sql
import os

db_name = 'Registro.db'
table_name = "Registro" 
fechaActual = datetime.now()
Fechahoy = datetime.strftime(fechaActual, "%Y-%m-%d")

def exportar():
    dt = datetime.now()
    FechaActual = datetime.strftime(dt, '%d/%m/%Y')
    HoraActual = datetime.strftime(dt, '%H:%M')
    am_or_pm = time.strftime("%p")
    desktopath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')    
    conn = sql.connect(db_name) 
    cursor = conn.cursor()
    query = cursor.execute("select * from {} ORDER BY Fecha DESC, Hora DESC".format(table_name))
    conn.commit()
    Nlist = []
    for row in query:
      row = list(row)
      Fechaobj = datetime.strptime(row[1], "%Y-%m-%d")
      Horaobj = datetime.strptime(row[9], "%H:%M:%S")
      Fecha = Fechaobj.toordinal() - datetime(1900, 1, 1).toordinal() + 2
      Hora = (Horaobj - datetime(1900, 1, 1)).total_seconds() / 86400  
      row = Fecha, Hora, row[2], row[3], row[4], row[5], row[6], row[7], row[8] 
      Nlist.append(tuple(row))
    columnas = ['Fecha', "Hora", 'Producto', 'Presentacion', 'Cantidad', 'Fragancia','Observaciones', 'PVPU', 'PVPT']
    df = pd.DataFrame(Nlist, columns = columnas)
    writer = pd.ExcelWriter(desktopath+'/Registro de ventas.xlsx', engine='xlsxwriter')
    workbook  = writer.book   
    df.to_excel(writer, sheet_name='Registro de ventas', startcol = 0, startrow = 13, index = False, na_rep='N/A')
    worksheet = writer.sheets['Registro de ventas']
    worksheet2 = workbook.add_worksheet('Estadisticas')
    Generado = f'GENERADO EL {FechaActual} A las {HoraActual} {am_or_pm}'
    merge_format1 = workbook.add_format({
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'font': 'Arial Black',
    'font_color': '#FFFFFF',
    'font_size': '22',
    'fg_color': '#76933C'})
    merge_format2 = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'font_color': '#000000',
    'font_size': '11',
    'fg_color': '#EEECE1'})
    MoneyFormat = workbook.add_format({'num_format': '$ #,##0.00'})
    TimeFormat = workbook.add_format({'num_format': 'hh:mm:ss AM/PM'})
    DateFormat = workbook.add_format({'num_format': 'yyyy-mm-dd'})
    worksheet.merge_range('A1:I12', '', merge_format1)
    worksheet.merge_range('A13:I13', Generado, merge_format2)
    worksheet.set_column('A:A', 17, DateFormat)
    worksheet.set_column('B:B', 12, TimeFormat)
    worksheet.set_column('C:C', 30)
    worksheet.set_column('D:D', 29)
    worksheet.set_column('E:E', 20)
    worksheet.set_column('F:F', 11)
    worksheet.set_column('G:G', 55)
    worksheet.set_column('H:H', 10, MoneyFormat)
    worksheet.set_column('I:I', 10, MoneyFormat)
    worksheet.autofilter("A14:I14")
    worksheet.insert_image(0,3, 'Archivos/imgs/Registro.png')
    ValueFormat = workbook.add_format({ 
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'font_color': '#000000',
    'font_size': '11',
    'fg_color': '#E4DFEC'}) 
    worksheet2.write('A1', 'Ventas AM', ValueFormat)
    worksheet2.set_column('A:A', 10)
    worksheet2.write('A2', 'Ventas PM', ValueFormat)

    maxcolumnhora = len(df["Hora"]) + 14

    worksheet2.write_formula('B1', f'''=COUNTIF('Registro de ventas'!B15:B{maxcolumnhora}, "<0,5") - COUNTIF('Registro de ventas'!B15:B4124,0)''', ValueFormat)
    worksheet2.write_formula('B2', f'''=COUNTIF('Registro de ventas'!B15:B{maxcolumnhora}, ">0,5")''', ValueFormat)

    chart1 = workbook.add_chart({'type': 'pie'})
    chart1.add_series({
     'name': 'Ventas AM/PM',
     'categories': '=Estadisticas!$A$1:$A$2',
     'values':     '=Estadisticas!$B$1:$B$2',
    }) 
    chart1.set_style(37)
    chart1.set_size({'width': 384, 'height': 360})
    worksheet2.insert_chart(5, 2, chart1) 
    worksheet2.hide_gridlines(2) 
    writer.save()
    os.startfile(desktopath+'/Registro de ventas.xlsx')
exportar()