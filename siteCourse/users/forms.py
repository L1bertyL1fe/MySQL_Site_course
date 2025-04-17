from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from allauth.account.forms import SignupForm

User = get_user_model()

class UserRegistrationForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput()
        self.fields['password1'].widget = forms.TextInput()
        self.fields['password2'].widget = forms.TextInput()


    # email = forms.EmailField(
    #     widget=forms.EmailInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Email'
    #     }),
    #     required=True
    # )
    # password1 = forms.CharField(
    #     widget=forms.PasswordInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Пароль'
    #     }),
    #     label="Пароль"
    # )
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Подтвердите пароль'
    #     }),
    #     label="Подтверждение пароля"
    # )
    #
    # class Meta:
    #     model = User
    #     fields = ['username', 'email', 'password1', 'password2']
    #     widgets = {
    #         'username': forms.TextInput(attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Имя пользователя'
    #         }),
    #     }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже используется")
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)