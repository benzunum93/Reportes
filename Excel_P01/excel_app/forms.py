from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django import forms
from django.template import RequestContext
import django_excel as excel

    
class UploadFileForm(forms.Form):
    file = forms.FileField()

    def upload(request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                filehandle = request.FILES['file']
                return excel.make_response(filehandle.get_sheet(), "csv")
            else:
                return HttpResponseBadRequest()
        else:
            form = UploadFileForm()
        return render(request,
                        'upload_form.html',
                        {'form': form}
                    )

    def download(request):
        sheet = excel.pe.Sheet([[1, 2],[3, 4]])
        return excel.make_response(sheet, "csv")

##Leemos datos de usuario para realizar operación
YEAR=[  '2010','2011','2012','2013','2014','2015','2016',
        '2017','2018','2019','2020','2021','2022','2023','2024',
        '2025','2026','2027','2028']
MONTHS = {
    1:('Jan'), 2:('Feb'), 3:('Mar'), 4:('Apr'),
    5:('May'), 6:('Jun'), 7:('jul'), 8:('Aug'),
    9:('Sep'), 10:('Oct'), 11:('Nov'), 12:('Dec')
    }

class Pilotosform(forms.Form):
    """
    |Se usa elegir que personal se le va a realizar el reporte
    """
    cantidad=forms.IntegerField(min_value=1)
    nombre=forms.CharField(max_length=200)
    apellido=forms.CharField(max_length=200)

    # A custom empty label with tuple
    fecha_inicial = forms.DateField(
        widget=forms.SelectDateWidget(years=YEAR,
                                    months=MONTHS, 
                                    ),
    )
    fecha_final = forms.DateField(
                    widget=forms.SelectDateWidget(
                                                years=YEAR,
                                                months=MONTHS, 
                                                )
                                )

class Cont_PersonasForm(forms.Form):
    """
    |Se usa el mismo form para el alojamiento y para el numero de personas
    """
    fuerza=forms.CharField(max_length=200)
    fecha_inicial = forms.DateField(
        widget=forms.SelectDateWidget(years=YEAR,
                                    months=MONTHS, 
                                    ),
    )
    fecha_final = forms.DateField(
                    widget=forms.SelectDateWidget(
                                                years=YEAR,
                                                months=MONTHS, 
                                                )
                                )



