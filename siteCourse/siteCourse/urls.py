from django.contrib import admin
from django.urls import path, include
from users.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('', include('courses.urls')),
    path('accounts/', include('allauth.urls')),
]
