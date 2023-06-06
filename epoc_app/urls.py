from django.urls import path
from .views import command, index
from .views import  Temp_serializer_agregar_data, command_serializer
from . import views 

urlpatterns = [
    path('snippets/',Temp_serializer_agregar_data,name ="Listado"),
    path('table',views.TableView.as_view(),name='table'),
    path('commands',views.command, name='command'),
    path('command_data',command_serializer, name='Command_list'),
    path('temp-chart/', views.temp_chart, name='temp-chart'),
    path('index/',index,name='home')
]