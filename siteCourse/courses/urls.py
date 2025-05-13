from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('module/theory/<int:module_id>/', views.module_theory, name='module_theory'),
    path('module/test/<int:module_id>/', views.module_test, name='module_test'),
    path('module/theory/edit/<int:module_id>/', views.edit_theory, name='edit_theory'),
    path('module/questions/edit/<int:module_id>/', views.edit_questions, name='edit_questions'),
    path('module/toggle/<int:module_id>/', views.toggle_module, name='toggle_module'),
]