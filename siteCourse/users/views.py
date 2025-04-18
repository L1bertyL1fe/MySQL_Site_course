from django.shortcuts import render
from allauth.account.views import SignupView
from .forms import CustomSignupForm
from allauth.account.views import LoginView
from .forms import CustomLoginForm
from django.contrib.auth import logout
from django.shortcuts import redirect

class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'registration.html'

def register_view(request):
    view = CustomSignupView.as_view()
    return view(request)

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'

def login_view(request):
    view = CustomLoginView.as_view()
    return view(request)

def logout_view(request):
    logout(request)
    return redirect('home')

def home_view(request):
    return render(request, 'index.html')