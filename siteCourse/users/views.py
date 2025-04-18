from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    logout(request)
    return redirect('home')

def home_view(request):
    return render(request, 'index.html')