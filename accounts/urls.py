from django.urls import path
from .views import signup_page

urlpatterns = [
    path("", signup_page, name="signup"),
]