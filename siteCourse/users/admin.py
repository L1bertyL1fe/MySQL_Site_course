from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('phone', 'role')}),
    )
    actions = ['make_teacher']

    def make_teacher(self, request, queryset):
        queryset.update(role='teacher')
        self.message_user(request, "Выбранные пользователи теперь преподаватели")
    make_teacher.short_description = "Сделать преподавателями"

admin.site.register(CustomUser, CustomUserAdmin)