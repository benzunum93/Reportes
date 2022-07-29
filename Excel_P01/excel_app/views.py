from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
#from _compact import JsonResponse
from django import forms
import django_excel as excel
from django.core.exceptions import *
#Forms excel_app
from excel_app.forms import Pilotosform
from excel_app.forms import UploadFileForm
from excel_app.forms import Cont_PersonasForm
#Models excel_app
from excel_app.models import Question, Choice
from guarda_excel import Manipular_excel
from fetchdata import fetch_main





data = [[1, 2, 3], [4, 5, 6]]





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
            return redirect('/excel_app/tipo_informe/')
            """ return excel.make_response(
                filehandle.get_sheet(), "csv", file_name="download"
            ) """
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


def download(request, file_type):
    sheet = excel.pe.Sheet(data)
    return excel.make_response(sheet, file_type)


def download_as_attachment(request, file_type, file_name):
    return excel.make_response_from_array(data, file_type, file_name=file_name)


def export_data(request, atype):
    if atype == "sheet":
        return excel.make_response_from_a_table(
            Question, "xls", file_name="sheet"
        )
    elif atype == "book":
        return excel.make_response_from_tables(
            [Question, Choice], "xls", file_name="book"
        )
    elif atype == "custom":
        question = Question.objects.get(slug="ide")
        query_sets = Choice.objects.filter(question=question)
        column_names = ["choice_text", "id", "votes"]
        return excel.make_response_from_query_sets(
            query_sets, column_names, "xls", file_name="custom"
        )
    else:
        return HttpResponseBadRequest(
            "Bad request. please put one of these "
            + "in your url suffix: sheet, book or custom"
        )


def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row

        if form.is_valid():
            request.FILES["file"].save_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[
                    ["question_text", "pub_date", "slug"],
                    {"Question": "question", "Choice": "choice_text", "Votes": "votes"},
                ],
            )
            return redirect("handson_view")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        "upload_form.html",
        {
            "form": form,
            "title": "Import excel data into database example",
            "header": "Please upload sample-data.xls:",
        },
    )


def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            request.FILES["file"].save_to_database(
                name_columns_by_row=2,
                model=Question,
                mapdict=["question_text", "pub_date", "slug"],
            )
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(request, "upload_form.html", {"form": form})


def exchange(request, file_type):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        filehandle = request.FILES["file"]
        return excel.make_response(filehandle.get_sheet(), file_type)
    else:
        return HttpResponseBadRequest()


def parse(request, data_struct_type):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        filehandle = request.FILES["file"]
        if data_struct_type == "array":
            return JsonResponse({"result": filehandle.get_array()})
        elif data_struct_type == "dict":
            return JsonResponse(filehandle.get_dict())
        elif data_struct_type == "records":
            return JsonResponse({"result": filehandle.get_records()})
        elif data_struct_type == "book":
            return JsonResponse(filehandle.get_book().to_dict())
        elif data_struct_type == "book_dict":
            return JsonResponse(filehandle.get_book_dict())
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


def handson_table(request):
    return excel.make_response_from_tables(
        [Question, Choice], "handsontable.html"
    )


def embed_handson_table(request):
    """
    Renders two table in a handsontable
    """
    content = excel.pe.save_book_as(
        models=[Question, Choice],
        dest_file_type="handsontable.html",
        dest_embed=True,
    )
    content.seek(0)
    return render(
        request,
        "custom-handson-table.html",
        {"handsontable_content": content.read()},
    )


def embed_handson_table_from_a_single_table(request):
    """
    Renders one table in a handsontable
    """
    content = excel.pe.save_as(
        model=Question, dest_file_type="handsontable.html", dest_embed=True
    )
    content.seek(0)
    return render(
        request,
        "custom-handson-table.html",
        {"handsontable_content": content.read()},
    )


def survey_result(request):
    question = Question.objects.get(slug="ide")
    query_sets = Choice.objects.filter(question=question)
    column_names = ["choice_text", "votes"]

    # Obtain a pyexcel sheet from the query sets
    sheet = excel.pe.get_sheet(
        query_sets=query_sets, column_names=column_names
    )
    sheet.name_columns_by_row(0)
    sheet.column.format("votes", int)

    # Transform the sheet into an svg chart
    svg = excel.pe.save_as(
        array=[sheet.column["choice_text"], sheet.column["votes"]],
        dest_file_type="svg",
        dest_chart_type="pie",
        dest_title=question.question_text,
        dest_width=600,
        dest_height=400,
    )

    return render(request, "survey_result.html", dict(svg=svg.read()))


def import_sheet_using_isave_to_database(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            request.FILES["file"].isave_to_database(
                model=Question, mapdict=["question_text", "pub_date", "slug"]
            )
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(request, "upload_form.html", {"form": form})


def import_data_using_isave_book_as(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row

        if form.is_valid():
            request.FILES["file"].isave_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[
                    ["question_text", "pub_date", "slug"],
                    {"Question": "question", "Choice": "choice_text", "Votes": "votes"},
                ],
            )
            return redirect("handson_view")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        "upload_form.html",
        {
            "form": form,
            "title": "Import excel data into database example",
            "header": "Please upload sample-data.xls:",
        },
    )


def import_without_bulk_save(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row

        if form.is_valid():
            request.FILES["file"].save_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[
                    ["question_text", "pub_date", "slug"],
                    ["question", "choice_text", "votes"],
                ],
                bulk_save=False,
            )
            return redirect("handson_view")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        "upload_form.html",
        {
            "form": form,
            "title": "Import excel data into database example",
            "header": "Please upload sample-data.xls:",
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
            fetch_main(data,reporte)
            return redirect('/excel_app')
        elif form.non_field_errors:
            print(f'Error in input')

    else:
        form= Pilotosform()
        print('Vacio')

    return render( request,"info/horas_pilotos.html", {
            "form": form,
            "title": "Horas"
        })




def contar_personas(request):
    if request.method =='POST':
        form=Cont_PersonasForm(request.POST)
                
        if form.is_valid():
             #Contiene un dictionary con los valores dados por el usuario
            data=form.cleaned_data
            #El #2 corresponde a contar_personas
            reporte=2
            fetch_main(data,reporte)
                
            return redirect('/excel_app/')
        
        elif form.non_field_errors:
            print(f'Error in input')

    else:
        form= Cont_PersonasForm()
        print('Vacio')

    return render( request,"info/num_personas.html",
        {
            "form": form,
            "title": "Contar personas"
        })