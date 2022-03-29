from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=30, required=False, help_text="Optional.", label="이름")
    username = forms.CharField(max_length=30, required=False, help_text="Optional.", label="닉네임")
    email = forms.EmailField(max_length=250, help_text="Required.", label="이메일")

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password1', 'password2', ]
