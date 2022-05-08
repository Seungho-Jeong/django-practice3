from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=30, required=False, help_text="Optional.", label="이름")
    username = forms.CharField(max_length=30, required=False, help_text="Optional.", label="닉네임")
    email = forms.EmailField(max_length=250, help_text="Required.", label="이메일")

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e-mail'}),
    )
    password = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': '_loginRememberMe'}),
        disabled=False,
    )