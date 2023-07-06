from django.urls import path
from .forms import LoginForm
from django.contrib.auth.views import LoginView

app_name = 'accounts'

urlpatterns = [
    path('', LoginView.as_view(template_name='registration/login.html', form_class=LoginForm), name='login')
]
