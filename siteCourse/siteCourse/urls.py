from django.contrib import admin
from django.urls import path, include
from users.views import home_view, CustomLoginView, logout_view, CustomSignupView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_view, name='home'),
    path('register/', CustomSignupView.as_view(), name='account_signup'),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('logout/', logout_view, name='logout'),
    path('accounts/', include('allauth.urls')),
]
