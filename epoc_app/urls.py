from django.urls import path
from django.conf.urls import re_path
from .views import index
from .views import  Temp_serializer_agregar_data, command_serializer
from . import views 

urlpatterns = [
    path('snippets/',Temp_serializer_agregar_data,name ="Listado"),
    path('table',views.TableView.as_view(),name='table'),
    path('command_data',command_serializer, name='Command_list'),
    path('temp-chart/<int:patient_id>/', views.temp_chart, name='temp-chart'),
    path('<int:patient_id>/', views.details_pat, name='detail'),
]