from datetime import datetime
import sqlite3
import pandas as pd
from datetime import datetime
import write_excel



def horas_pilotos(lista_nombres,columna, cur):
    """
    |Fetch for hour of each person
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
    |Calle by the function 'fechas' Count people are in the desired column a
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
    |Fetch data for given dates
    """    

    #Select the table name "Entrenamientos" and the column "Fecha"
    #And find the values Between "date_ini" and "date_final"
    
    Fuerza=Fuerza.lower()
    
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

    
    
def fetch_main(data,reporte):
    try:
        print(data)
    except:
        pass
    try:
        #Connection to the DB
        name_db='EntrenamientosDB.sqlite'    
        conn = sqlite3.connect(name_db)
        
        with conn:

            cur = conn.cursor()
            
            
            if reporte==1:
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
            
            elif reporte==2:
                fechas(data['fecha_inicial'],data['fecha_final'],data['fuerza'],cur)
                
            
            
            
    
    except ConnectionError as e:
        raise RuntimeError('Failed to open database') from e

    except OSError:
        print(f'OSError database dont exists')
        raise RuntimeError from None 

""" if __name__=='__main__':


    ###################################################
    #This is the data that is fetch from the web and to be get from another
    #proyect
    lista=['melgarejo mauricio','Arango Juan','']
    #Tipo de reporte
    reporte=1
                #Year, Month, Day
    date_ini=   datetime(2022,2,2)
    date_final= datetime(2022,2,5)

    #date_ini= '-'.join(date_ini)
    #date_final= '-'.join(date_final)

    Fuerza='ejc'
    #######################################################
    #Count hours of each pilot
    fetch_main(lista,reporte)
    #Count people in a given frametime
 """
    