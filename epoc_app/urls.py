from django.urls import path
from . import views 

urlpatterns = [
    path('snippets/',views.Spo2_serializer_agregar_data,name ="Listado"),
    path('command_data/<str:name>/',views.command_serializer, name='Command_list'),
    path('temp-chart/<int:patient_id>/', views.spo2_chart, name='spo2-chart'),
    path('monitor/<str:name>/', views.details_pat, name='detail'),
    path('monitor/', views.monitor, name='monitor'),
    path('admin/', views.admin, name='admin'),
    path('add-user/', views.add_user, name='add_user'),
    path('<uuid:uuid>/edit/', views.edit_user, name='edit_user'),
    path('<str:uuid>/delete/', views.delete_user, name='delete_user'),

]