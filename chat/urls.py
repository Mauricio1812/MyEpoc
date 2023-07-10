from django.urls import path

from . import views 

app_name = 'chat'

urlpatterns = [
    path('api/create-room/<str:uuid>/', views.create_room, name='create-room'),
    path('<str:uuid>/', views.room, name='room'),
    path('<str:uuid>/delete/', views.delete_room, name='delete_room'),
]