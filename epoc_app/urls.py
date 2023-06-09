from django.urls import path
from django.conf.urls import re_path
from .views import index
from .views import  Temp_serializer_agregar_data, command_serializer
from . import views 

urlpatterns = [
    path('snippets/',Temp_serializer_agregar_data,name ="Listado"),
    path('table',views.TableView.as_view(),name='table'),
    path('command_data',command_serializer, name='Command_list'),
    re_path(r'^temp-chart/(?P<patient_id>[0-9]+)/$', views.temp_chart, name='temp-chart'),
    re_path(r'^(?P<patient_id>[0-9]+)/$', views.details_pat, name='detail'),
    #path('index/',index,name='home')
]