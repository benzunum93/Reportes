import os
from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    #path('admin/', admin.site.urls),
    path(os.getenv('SECRET_ADMIN_URL') + '/admin/', admin.site.urls),
    path('excel_app/', include('excel_app.urls'))
]
