from datetime import datetime
#import re
import sqlite3
from xmlrpc.client import DateTime
#from xmlrpc.client import DateTime
import pandas as pd
#Escribe y genera archivos en excel
import write_excel
#Manejar fechas
from datetime import date, timedelta


def horas_pilotos(nombres,columna, cur):
    """
    |Count how many hours a person has flight the simulator
    |and create a report in excel with the name, and the hours
    |in each position
    """
    horas=0
  
    #Select the table name "Entrenamientos" with the column "columna"
    #And find the values that match "lista_nombres"
    lista_nombres=[nombres.lower()]
    
    cur.execute("SELECT * FROM Entrenamientos WHERE "+columna+"=?", (lista_nombres))
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
        if row[columna]!=None and row[columna]!='arango juan' :
            
            #Count people and save it in "num_person"
            if row[columna] not in num_person:
                num_person[row[columna]]=1
            else:
                num_person[row[columna]]=num_person[row[columna]]+1
        
            
    
    return num_person


def fechas(date_ini:str,date_final:DateTime, Fuerza:str,cur):
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
    
    start_date=date_ini
    end_date=date_final
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    
    personal=dict()
    for single_date in daterange(start_date, end_date):
        fecha=single_date.strftime("%Y-%m-%d")
        
    
        #Select the table name "Entrenamientos" and the column "Fecha"
        #and search the people Between "date_ini" and "date_final", and
        #respectively force
        #Arreglo de fechas para consultar en la DB
        
        fecha_ini=str(fecha)+' 00:00:00'
        fecha_final=str(fecha)+' 23:59:59'    
        cur.execute("SELECT * FROM Entrenamientos WHERE Fecha BETWEEN ? And ? And Fuerza=? ",(fecha_ini,fecha_final,Fuerza))
        
        #cur.execute("SELECT * FROM Entrenamientos WHERE CONVERT(DATETIME, Fecha)=? AND Fuerza=?",(date_ini,Fuerza))
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
        #Save for date the names and the count of people that train in that day
        personal[fecha]=num_personas
        #Write a reporter in excel with the fetchdata
        #write_excel.conteo_personas(num_personas, Fuerza)
    
    return personal


def reporte_horas_fac(date_ini:str,date_final:str,cur):
    """
    |Fetch data from the Fuerza 'Fac' between two dates
    - cur -> is the cursor from the database
    """
    cur.execute("SELECT * FROM Entrenamientos Where Fecha BETWEEN ? And ? And Fuerza=?",(date_ini,date_final,'fac'))
    rows = cur.fetchall()
    
    try:
        df=pd.DataFrame(rows)
        df=df.iloc[:,1:22]
        
        df.columns=['Fecha','Grado1','Instructor','Grado2','Piloto','Grado3',
            'CoPiloto','Grado4','Observador','Hora_Entrada','Hora_Salida',
            'Horas','Calificacion','VFR','IFR','NVR','Observaciones',
            'Tipoentrenamiento', 'Fuerza','Tipo','Unidad']
            
        hospedaje=pd.Series([])
        for i in range(len(df)):
            hospedaje[i]='N/A'
        df.insert(3, 'Hospedaje', hospedaje)
        df.insert(6, 'Hospedaje2', hospedaje)
        df.insert(9, 'Hospedaje3', hospedaje)
        df.insert(12, 'Hospedaje4', hospedaje)
    except ValueError:
        print('###########Error: No Data Fetched #############')

    cur.execute("SELECT * FROM Entrenamientos Where Fecha BETWEEN ? And ? And Fuerza=?",(date_ini,date_final,'fab'))
    data_fab = cur.fetchall()
     
    try:
        
        df_fab=pd.DataFrame(data_fab)
        df_fab=df_fab.iloc[:,1:22]

        
        df_fab.columns=['Fecha','Grado1','Instructor','Grado2','Piloto','Grado3',
            'CoPiloto','Grado4','Observador','Hora_Entrada','Hora_Salida',
            'Horas','Calificacion','VFR','IFR','NVR','Observaciones',
            'Tipoentrenamiento', 'Fuerza','Tipo','Unidad']
        
        hospedaje=pd.Series([])
        for i in range(len(df_fab)):
            hospedaje[i]='N/A'
        df_fab.insert(3, 'Hospedaje', hospedaje)
        df_fab.insert(6, 'Hospedaje2', hospedaje)
        df_fab.insert(9, 'Hospedaje3', hospedaje)
        df_fab.insert(12, 'Hospedaje4', hospedaje)
        
        #Une las dos tablas y organiza por fechas
        tablas=pd.concat([df,df_fab])
        tablas['Fecha'] = pd.to_datetime(tablas['Fecha'])
        
        
        #Organiza la tabla por fechas
        tablas=tablas.sort_values(by='Fecha')
        
        

        #Envia la tabla para ser escrita en excel
        write_excel.reporte_fac(tablas)
        #write_excel.reporte_fac(df,df_fab)
    except ValueError:
        print('###########Error: No Data Fetched #############')
    


def reporte_horas_ejc(date_ini:str,date_final:str,cur):
    """
    |Fetch data from the Fuerza 'Ejc' between two dates
    - cur -> is the cursor from the database
    """
    cur.execute("SELECT * FROM Entrenamientos Where Fecha BETWEEN ? And ? And Fuerza=? ",(date_ini,date_final,'ejc'))
    rows = cur.fetchall()
    
    try:
        df=pd.DataFrame(rows)
        
        df=df.iloc[:,1:22]
        
        df.columns=['Fecha','Grado1','Instructor','Grado2','Piloto','Grado3',
            'CoPiloto','Grado4','Observador','Hora_Entrada','Hora_Salida',
            'Horas','Calificacion','VFR','IFR','NVR','Observaciones',
            'Tipoentrenamiento', 'Fuerza','Tipo','Unidad']
        #Vuelve los valores de la columna Fecha en Datetime
        
        df['Fecha'] = pd.to_datetime(df['Fecha'])    
        
        #Corriege las horas a mostrar
        for n in range(len(df)):
            hora1=df['Hora_Entrada'][n]
            hora1=hora1[:5]
            df['Hora_Entrada'][n]=hora1
            
        
        #Corriege las horas a mostrar
        for f in range(len(df)):
            hora2=df['Hora_Salida'][f]
            hora2=hora2[:5]
            df['Hora_Salida'][f]=hora2
        
            
        
        hospedaje=pd.Series([]).astype(str)
        
        #Marca con un "Si" si las horas son tipo A y con un "No" si son tipo B
        #Luego crea cuatro columnas y las agrega a tabla de datos
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
    except ValueError:
        print('###########Error: No Data Fetched #############')
    

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
                
                data['nombre']=data['apellido']+' '+data['nombre']
                
                
                #print('Generando reporte de horas de ', data['nombre'])
                total=dict()
                
                
                total['Instructor']=horas_pilotos(data['nombre'],"Instructor",cur)
                total['Piloto']=horas_pilotos(data['nombre'],"Piloto",cur)
                total['CoPiloto']=horas_pilotos(data['nombre'],"CoPiloto",cur)
                total['Observador']=horas_pilotos(data['nombre'],"Observador",cur)
                total['Total']=0        
                for values in total.keys():
                    if values != 'Total':
                        total['Total']=total['Total']+total[values]
                
                write_excel.horas_pilotos(data['nombre'],total)
                return(data['nombre'],total)

            #Reporte de conteo de personas entrenadas en fecha especifica
            elif reporte==2:
                #print('Generando reporte Conteo de personas...')
                num_personas=fechas(data['fecha_inicial'],data['fecha_final'],data['fuerza'],cur)
                return(num_personas)
            #Reporte mensual EJC
            elif reporte==3:
                #print('Generando reporte EJC...')
                reporte_horas_ejc(data['fecha_inicial'],data['fecha_final'],cur)
            
            #Reporte mensual FAC
            elif reporte==4:
                #print('Generando reporte FAC...')
                reporte_horas_fac(data['fecha_inicial'],data['fecha_final'],cur)
            
            
    
    except ConnectionError as e:
        raise RuntimeError('Failed to open database') from e

    except OSError:
        print(f'OSError database dont exists')
        raise RuntimeError from None 

