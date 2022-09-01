from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
#from _compact import JsonResponse
from django import forms
from django.core.exceptions import *
#Forms ciac_app
from ciac_app.forms import Pilotosform
from ciac_app.forms import UploadFileForm
from ciac_app.forms import Cont_PersonasForm
from ciac_app.forms import Reporte_mensualForm
#Models ciac_app
from ciac_app.models import Question, Choice
#Archivos de codigos
from guarda_excel import Manipular_excel
from fetchdata import fetch_main
#Work with excel.xlsx files
import xlsxwriter

# Create your views here.
def upload(request):
    """
    |Carga un archivo excel a la base de datos.
    """
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES["file"]
            #Send file to guardar_excel.py
            Manipular_excel(filehandle)
            return redirect('/ciac_app/tipo_informe')
            
    else:
        form = UploadFileForm()
    return render(
        request,
        "upload_form.html",
        {
            "form": form,
            "title": "Excel file upload"
        },
    )
    

##################################################################
# Entrada usuario 
def tipo_informe(request):
    """Elige el tipo de informe a realizar"""
    return render(request, 'info/tipo_informe.html')



def search(request):
    """
    |Usado para contar las horas voladas de un piloto en un periodo de tiempo 
    |determinado.
    |
    |Recibe los valores input por el usuario para hacer un query en la base
    |de datos
    """     
    if request.method =='POST':
        form=Pilotosform(request.POST)
                
        if form.is_valid():
                       
            #Contiene un dictionary con los valores dados por el usuario
            data=form.cleaned_data
            
            reporte=1
            name,horas=fetch_main(data,reporte)
            #print('##Nombre: ',name,'Horas: ',horas)
            context= {
                'personas': name,
                'horas': horas,
                
                }
            
            return render(request,'info/resultado_horas_pilotos.html', context)    
            #return redirect('/ciac_app')
        elif form.non_field_errors:
            print(f'Error in input')

    else:
        form= Pilotosform()
        #print('Vacio')

    return render( request,"info/horas_pilotos.html", {
            "form": form,
            "title": "Horas"
        })




def contar_personas(request):
    """
    |Cuenta la cantidad de personas que han entrenado en un periodo determinado
    |por fuerza
    """
    if request.method =='POST':
        form=Cont_PersonasForm(request.POST)
                
        if form.is_valid():
            #Contiene un dictionary con los valores dados por el usuario
            data=form.cleaned_data
            #print(data)
            #El #2 corresponde a contar_personas
            reporte=2
            num_personas=fetch_main(data,reporte)
            #Guarda la informacion para luego ser enviada a un render en
            #HTML
            list=dict()
            for key, value in num_personas.items():
                list[key]=len(value)
                
            
            context= {
                'personas': list,
                
                'fuerza':data
                }
            
            return render(request,'info/resultado_conteo.html', context)    
            #return redirect('/ciac_app/')
        
        elif form.non_field_errors:
            print(f'Error in input')

    else:
        form= Cont_PersonasForm()
        #print('Vacio')

    return render( request,"info/num_personas.html",
        {
            "form": form,
            "title": "Contar personas"
        })



def reporte_horas_ejc(request):
    
    if request.method =='POST':
        form=Reporte_mensualForm(request.POST)
                
        if form.is_valid():
            #Contiene un dictionary con los valores dados por el usuario
            data=form.cleaned_data
            
            #El #3 corresponde a reporte_ejc
            reporte=3
            fetch_main(data,reporte)

            filename='Reporte del Mes EJC'
            extension='.xlsx'
            filename=filename+extension
            path='D:/Sebastian/Course python/Django/Ciac_web_page/ciac_venv/ciac_set/'+filename
            #Download the Excel File in the filename from the given directory
            try:
                with open(path, 'rb') as f:
                    response=HttpResponse(f.read(),content_type='application/ms-excel')
                    response['Content-Disposition'] = 'attachment; filename='+filename
                    
                    return response
                    
            except Exception as Error:
                return HttpResponse(Error)
            
                
            #return redirect('/ciac_app/')
        
        elif form.non_field_errors:
            print(f'Error in input')

    else:
        form= Reporte_mensualForm()
        #print('Vacio')

    return render( request,"info/reporte_mensualEJC.html",
        {
            "form": form,
            "title": "Reporte EJC"
        })


def reporte_horas_fac(request):
    if request.method =='POST':
        form=Reporte_mensualForm(request.POST)
                
        if form.is_valid():
            #Contiene un dictionary con los valores dados por el usuario
            data=form.cleaned_data
            
            
            #El #4 corresponde a reporte FAC-FAB
            reporte=4
            fetch_main(data,reporte)
            filename='Reporte del Mes FAC-FAB'
            extension='.xlsx'
            filename=filename+extension
            path='D:/Sebastian/Course python/Django/Ciac_web_page/ciac_venv/ciac_set/'+filename
            #Download the Excel File in the "filename" from the given directory in "path"
            try:
                with open(path, 'rb') as f:
                    response=HttpResponse(f.read(),content_type='application/ms-excel')
                    response['Content-Disposition'] = 'attachment; filename='+filename
                    
                    return response
                    
            except Exception as Error:
                return HttpResponse(Error)
            
            #return redirect('/ciac_app/')
        
        elif form.non_field_errors:
            print(f'Error in input')

    else:
        form= Reporte_mensualForm()
        #print('Vacio')

    return render( request,"info/reporte_mensualFAC.html",
        {
            "form": form,
            "title": "Reporte FAC"
        })