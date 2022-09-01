"""ciac_set URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from user_authen import views as user_view
from django.contrib.auth import views as auth
urlpatterns = [
    path('admin/', admin.site.urls),
    #URL app
    path('ciac_app/', include('ciac_app.urls')),
    ##### user related path########################## 
    path('user/', include('user_authen.urls')),
    path('login/', user_view.Login, name ='login'),
    #Envia a index de user_authen
    path('logout/', auth.LogoutView.as_view(template_name ='user/index.html'), name ='logout'),
    path('register/', user_view.register, name ='register'),
]
