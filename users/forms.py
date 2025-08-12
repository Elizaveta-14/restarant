from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    phone = forms.CharField(required=False, label="Телефон")

    class Meta:
        model = User
        fields = ['email', 'phone', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
