from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm, LoginForm as AllAuthLoginForm

User = get_user_model()
class CustomSignupForm(SignupForm):

    role = forms.ChoiceField(
        choices=[
            ('student', 'Студент'),
            ('teacher', 'Преподаватель'),
        ],
        label='Выберите роль',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Имя пользователя'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        })

    def save(self, request):
        user = super().save(request)
        selected_role = self.cleaned_data.get('role')

        if selected_role == 'teacher':
            # Создаем запрос на подтверждение роли преподавателя
            TeacherRequest.objects.create(user=user)
            messages.info(
                request,
                'Ваша заявка на роль преподавателя отправлена на рассмотрение. '
                'Вы получите уведомление после подтверждения администратором.'
            )
            # Временно сохраняем как студента
            user.role = 'student'
        else:
            user.role = selected_role

        user.save()
        return user




class CustomLoginForm(AllAuthLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['login'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Имя пользователя или e-mail'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })

        self.fields['remember'].widget.attrs.update({
            'class': 'form-check-input'
        })
