from django.urls import path
from ciac_app import views
from django.conf import settings #Importar archivo de conf de django
from django.contrib.staticfiles.urls import static #Para manejar archivos estaticos como imagenes

urlpatterns = [
    path('', views.upload, name='Add_file'),
    
    #Choose what kind of data the user want
    path('tipo_informe/', views.tipo_informe,name="Tipo_informe"),
    #Horas Pilotos    
    path('horas/', views.search,name="Horas"),
    #Conteo de personas
    path('conteo/', views.contar_personas,name="Conteo"),

    path('reporteFAC/', views.reporte_horas_fac,name="Reporte_FAC_FAB"),
    path('reporteEJC/', views.reporte_horas_ejc,name="Reporte_EJC"),
    path('view_result/', views.contar_personas, name = 'view_result'),
    path('result_horas_pilotos/', views.search, name = 'result_horas_pilotos'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)