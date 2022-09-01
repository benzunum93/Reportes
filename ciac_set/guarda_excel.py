import pandas as pd
import xlsxwriter
#Para utilizar base de datos
import sqlite3 




def Manipular_excel(path_file):
    """
    |Take a Excel file imported from a user in a web
    """
    
    #Sheet name in the Excel file
    hoja= "Entrenamientos" 
    #Types of values in the columns, you need to be aware that the columns names
    #don't have to have any spaces.
    col_types ={'Instructor':str,'Piloto':str, "Co-Piloto":str,"Horas":float}
    #DB named where it will be storage the data
    name_db='EntrenamientosDB.sqlite'
    #Table name in the DB
    Table_db='Entrenamientos'

    try:
        #If file have format .csv save it as .xlsx
        #Remember to change the date for the corresponding Year
        pd.read_csv('CUADRO DE CONTROL 2022.csv').to_excel(path_file, index=False)
        
    except:
        pass
        
    try:
        #Read the file and pass it as a pandas frame
        df=pd.read_excel(path_file, sheet_name=hoja, dtype=col_types)
        #Get columns from 1 to 21 only
        df=df.iloc[:,:21]
        #Give a name to each column
        df.columns=['Fecha','Grado1','Instructor','Grado2','Piloto','Grado3',
        'CoPiloto','Grado4','Observador','Hora_Entrada','Hora_Salida',
        'Horas','Calificacion','VFR','IFR','NVR','Observaciones',
        'Tipoentrenamiento', 'Fuerza','Tipo','Unidad']
        #Made all the str values lowercase
        try:
            df['Instructor']=   df['Instructor'].str.lower()
            df['Piloto']=       df['Piloto'].str.lower()
            df['CoPiloto']=     df['CoPiloto'].str.lower()
            df['Observador']=   df['Observador'].str.lower()
            df['Fuerza']=       df['Fuerza'].str.lower()
            df['Unidad']=       df['Unidad'].str.lower()
            
            
            
        except:
            print('Falla en la lectura de la columna')
    except FileNotFoundError:
        #If the file doesn't exist
        print("File could not be found")
                   
    
    try:
        """
        |Connection to the DB Sqlite
        """
        #Conection to the DB
        conn = sqlite3.connect(name_db)
        #Storage the pd frame a DB.
        df.to_sql(Table_db,conn, if_exists="replace")
        conn.commit()
        conn.close()
    except ConnectionError as e:
        raise RuntimeError('Failed to open database') from e
    except OSError:
        print(f'OSError database dont exists')
        raise RuntimeError from None 

