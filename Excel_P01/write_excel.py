import sqlite3
from tkinter.font import BOLD
import pandas as pd
from datetime import datetime
import xlsxwriter



def conteo_personas(personas,Fuerza):

    

    workbook= xlsxwriter.Workbook('Reporte_conteo.xlsx')

    # Formato de titulo
    formato_titulo = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#333f4f',
        'font_color': 'white',
        'text_wrap': True})
    # Formato de variables
    formato_variables = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'top',
        'fg_color': '#ddebf7',
        'font_color': 'black',
        'text_wrap': True})
    # Formato del texto normal
    formato_normal = workbook.add_format({
        'border': 1,
        'align': 'left',
        'valign': 'top',
        'text_wrap': True})
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})
    
    
    Unidad=str(Fuerza).capitalize()
    worksheet = workbook.add_worksheet(Unidad)
    worksheet.merge_range('A2:B2', 'Tripulaciones',formato_variables)
    #Write in multiples rows, and it used for the title
    worksheet.merge_range('A1:B1', Unidad,formato_titulo)
    i,j=2,1 #Fila=i, Columna=j
    for per in personas:
        worksheet.set_column(i, 0, 20)
        per= str(per).upper()
        worksheet.write(i,j, per,formato_normal)
        i+=1
    worksheet.write(i, j-1, 'Total',formato_variables)
    worksheet.write(i,j, len(personas),formato_normal)

    workbook.close()

def horas_pilotos(nombre,horas):
    workbook= xlsxwriter.Workbook('Reporte_Horas.xlsx')
    # Formato de titulo
    formato_titulo = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#333f4f',
        'font_color': 'white',
        'text_wrap': True})
    # Formato de variables

    name_pilot=str(nombre).capitalize()
    if 'Horas' in workbook.sheetnames:
        print('Horas exists')
        worksheet = workbook.add_worksheet('Horas_2')
    else:
        worksheet = workbook.add_worksheet('Horas')
    #Create a title with the variable 'nombre'
    worksheet.merge_range('A1:B1', name_pilot,formato_titulo)
    i,j=1,0 #Fila=i, Columna=j
    
    for name in horas:
        
        worksheet.set_column(i, 0, 15)
        worksheet.write(i,j, name)
        worksheet.write(i,j+1, horas[name])
        i+=1

    workbook.close()