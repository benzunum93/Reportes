from datetime import datetime
import re
import sqlite3
import pandas as pd
from datetime import datetime
import write_excel



def horas_pilotos(lista_nombres,columna, cur):
    """
    |Count how many hours a person has flight the simulator
    |and create a report in excel with the name, and the hours
    |in each position
    """
    horas=0
  
    #Select the table name "Entrenamientos" with the column "columna"
    #And find the values that match "lista_nombres"
    
    cur.execute("SELECT * FROM Entrenamientos WHERE "+columna+"=?", (lista_nombres[0],))
    rows = cur.fetchall()
    
    for row in rows:
        #The 12 is the "Horas# column
        horas=float(row[12])+horas
    
    return horas

    
    

def contar_personas(datos,columna:int,num_person:dict)-> dict:
    """
    |Called by the function 'fechas' to count the people that are in the desired column
    
    """
    
    for row in datos:
        
        #If the value it's not empty
        if row[columna]!=None:
            
            #Count people and save it in "num_person"
            if row[columna] not in num_person:
                num_person[row[columna]]=1
            else:
                num_person[row[columna]]=num_person[row[columna]]+1        
    
    return num_person


def fechas(date_ini:str,date_final:str, Fuerza:str,cur):
    """
    |Send the input data for given dates, then counts how many people are in a given date
    |passing to the function 'contar_personas' the data in the database, the number of 
    |the column to be search for the information and a varible 'num_personas' that will storage 
    |the count of people.
    |The made a report to excel with the names and the count of people
    - cur -> is the cursor from the database
    - Fuerza -> str
    - num_personas -> int, count the people
    
    """    

  
    
    Fuerza=Fuerza.lower()
    
    #Select the table name "Entrenamientos" and the column "Fecha"
    #and search the people Between "date_ini" and "date_final", and
    #respectively force
        
    cur.execute("SELECT * FROM Entrenamientos Where Fecha BETWEEN ? And ? And Fuerza=? ",(date_ini,date_final,Fuerza))
    rows = cur.fetchall()
    
    #Count people in the desired colums
    num_personas=dict()
    #Instructor
    num_personas=contar_personas(rows,3, num_personas)
    #Piloto
    num_personas=contar_personas(rows,5, num_personas)
    #Co-Piloto
    num_personas=contar_personas(rows,7, num_personas)
    #Observador
    num_personas=contar_personas(rows,9, num_personas)
    #Write a reporter in excel with the fetchdata
    write_excel.conteo_personas(num_personas, Fuerza)

def reporte_horas_fac(date_ini:str,date_final:str,cur):
    """
    |Fetch data from the Fuerza 'Fac' between two dates
    - cur -> is the cursor from the database
    """
    cur.execute("SELECT * FROM Entrenamientos Where Fecha BETWEEN ? And ? And Fuerza=? ",(date_ini,date_final,'fac'))
    rows = cur.fetchall()
    write_excel.reporte_fac(rows)
    

def reporte_horas_ejc(date_ini:str,date_final:str,cur):
    """
    |Fetch data from the Fuerza 'Ejc' between two dates
    - cur -> is the cursor from the database
    """
    cur.execute("SELECT * FROM Entrenamientos Where Fecha BETWEEN ? And ? And Fuerza=? ",(date_ini,date_final,'ejc'))
    rows = cur.fetchall()
    df=pd.DataFrame(rows)
    df=df.iloc[:,1:22]
    
    df.columns=['Fecha','Grado1','Instructor','Grado2','Piloto','Grado3',
        'CoPiloto','Grado4','Observador','Hora_Entrada','Hora_Salida',
        'Horas','Calificacion','VFR','IFR','NVR','Observaciones',
        'Tipoentrenamiento', 'Fuerza','Tipo','Unidad']
    for i in range(len(df['Fecha'])):
        fecha=df['Fecha'][i]
        fecha=fecha.split()
        df['Fecha'][i]=fecha[0]
        
    
    for n in range(len(df)):
        hora1=df['Hora_Entrada'][n]
        hora1=hora1[:5]
        df['Hora_Entrada'][n]=hora1
        
    

    for f in range(len(df)):
        hora2=df['Hora_Salida'][f]
        hora2=hora2[:5]
        df['Hora_Salida'][f]=hora2
    
        
    
    hospedaje=pd.Series([])
    
    
    for i in range(len(df)):
        if df['Tipo'][i]=='A':
            hospedaje[i]='SI'
        else:
            hospedaje[i]='NO'
    df.insert(3, 'Hospedaje', hospedaje)
    df.insert(6, 'Hospedaje2', hospedaje)
    df.insert(9, 'Hospedaje3', hospedaje)
    df.insert(12, 'Hospedaje4', hospedaje)
    
    write_excel.reporte_ejc(df)
    

    

def fetch_main(data,reporte):
    """
    |Get all the inputs from the user and is storage in a
    |Dictionary named 'data', also read what kind of report
    |is needed, and send a query to the DB to retrive the information
    |needed.
    -Data   -> dict()
    -reporte-> int
    -Database-> Sqlite
    
    """
    
    try:
        #Connection to the DB
        name_db='EntrenamientosDB.sqlite'    
        conn = sqlite3.connect(name_db)
        
        with conn:

            cur = conn.cursor()
            
            #Reporte de horas Voladas
            if reporte==1:
                print('Generando reporte de horas de ', data['nombre'])
                total=dict()
                total['Instructor']=horas_pilotos(data['nombre'],"Instructor",cur)
                total['Piloto']=horas_pilotos(data['nombre'],"Piloto",cur)
                total['Co-Piloto']=horas_pilotos(data['nombre'],"CoPiloto",cur)
                total['Observador']=horas_pilotos(data['nombre'],"Observador",cur)
                total['Total']=0        
                for values in total.keys():
                    if values != 'Total':
                        total['Total']=total['Total']+total[values]

                write_excel.horas_pilotos(data['nombre'],total)
            #Reporte de conteo de personas entrenadas en fecha especifica
            elif reporte==2:
                print('Generando reporte Conteo de personas...')
                fechas(data['fecha_inicial'],data['fecha_final'],data['Fuerza'],cur)
            #Reporte mensual EJC
            elif reporte==3:
                print('Generando reporte EJC...')
                reporte_horas_ejc(data['fecha_inicial'],data['fecha_final'],cur)
            
            #Reporte mensual FAC
            elif reporte==4:
                print('Generando reporte FAC...')
                reporte_horas_fac(data['fecha_inicial'],data['fecha_final'],cur)
            
            
    
    except ConnectionError as e:
        raise RuntimeError('Failed to open database') from e

    except OSError:
        print(f'OSError database dont exists')
        raise RuntimeError from None 

if __name__=='__main__':
    ###################################################
    #This is the data that is need to be fetch from the web
    # all the get data is storage in a ditionary and then it
    #query the DB
    
    #Tipo de reporte, 1 conteo de horas, 2 conteo de personas, 3 reporte ejc,4 reporte fac
    reporte=3

    data=dict()
    data['nombre']='melgarejo mauricio'
    
                #Year, Month, Day
    try:

        data['fecha_inicial']=datetime(2022,7,1)
    except ValueError as e:
        print(f'Values Error {e}')
    try:
        data['fecha_final']= datetime(2022,7,31)
    except ValueError as e:
        print(f'Values Error {e}')
    
    data['Fuerza']='ejc'

    #######################################################
    #Send a query to be fetch in a DB
    fetch_main(data,reporte)
    
