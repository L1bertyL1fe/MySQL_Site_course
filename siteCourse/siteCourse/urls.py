from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from users.views import register_view, home_view, login_view, authentication_auth_login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', authentication_auth_login_view, name='authentication.auth-login'),

]