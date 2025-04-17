from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView

from .forms import LoginForm

class Views(TemplateView):
    pass

authentication_auth_login_view = Views.as_view(template_name="login.html")

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})

def home_view(request):
    return render(request, 'index.html')

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html', {'form': form})