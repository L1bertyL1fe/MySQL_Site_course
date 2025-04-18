from django.contrib import admin
from django.urls import path, include
from users.views import register_view, home_view, CustomLoginView, logout_view, login_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_view, name='home'),
    path('register/', register_view, name='account_signup'),
    path('accounts/login/', login_view, name='account_login'),
    path('logout/', logout_view, name='logout'),
    path('accounts/', include('allauth.urls')),
]
