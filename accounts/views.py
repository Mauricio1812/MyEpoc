from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth import login, authenticate
from . import forms

# def signup_page(request):
#     form = forms.SignupForm()
#     if request.method == 'POST':
#         form = forms.SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()
#             user.profile.first_name = form.cleaned_data.get('first_name')
#             user.profile.last_name = form.cleaned_data.get('last_name')
#             user.profile.email = form.cleaned_data.get('email')
#             user.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect(settings.LOGIN_REDIRECT_URL)
#     return render(request, 'registration/signup.html', context={'form': form})

