"""
URL configuration for MyEpoc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from epoc_app.views import welcome

admin.site.site_header = "Portal SPO2"
admin.site.site_title = "Portal SPO2"
admin.site.index_title = "Bienvenido al sistema de registro de SPO2 "

urlpatterns = [
    path('epoc/', include('epoc_app.urls')),
    path('chat/', include('chat.urls')),
    path('login/', include('accounts.urls'), name='login'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path("", welcome, name="welcome"), 
]
