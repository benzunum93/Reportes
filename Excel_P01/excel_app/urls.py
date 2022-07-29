from django.urls import path
from excel_app import views


urlpatterns = [
    path('', views.upload, name='uplink'),
    path('download/(.*)', views.download, name="download"),
    path('download_attachment/(.*)/(.*)', views.download_as_attachment,
        name="download_attachment"),
    path('exchange/(.*)', views.exchange, name="exchange"),
    path('parse/(.*)', views.parse, name="parse"),
    path('import/', views.import_data, name="import"),
    path('import_sheet/', views.import_sheet, name="import_sheet"),
    path('export/(.*)', views.export_data, name="export"),
    path('handson_view/', views.handson_table, name="handson_view"),

    # handson table view
    path('embedded_handson_view/',
        views.embed_handson_table, name="embed_handson_view"),
    path('embedded_handson_view_single/',
        views.embed_handson_table_from_a_single_table,
        name="embed_handson_view"),
    # survey_result
    path('survey_result/',
        views.survey_result, name='survey_result'),

    # testing purpose
    path('import_using_isave/',
        views.import_data_using_isave_book_as),
    path('import_sheet_using_isave/',
        views.import_sheet_using_isave_to_database),
    path('import_without_bulk_save/',
        views.import_without_bulk_save, name="import_no_bulk_save"),
    
    
    #Choose what kind of data the user want
    path('tipo_informe/', views.tipo_informe,name="Tipo_informe"),
    #Horas Pilotos    
    path('horas/', views.search,name="Horas"),
    #Conteo de personas
    path('conteo/', views.contar_personas,name="Conteo"),
    
]
