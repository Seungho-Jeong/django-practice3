from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        message = "Invalid data."

        if form.is_valid():
            form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            message = "Successfully Signup."
        return render(request, 'register.html', {'form': form, 'message': message})

    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})


def login_view(request):
    message = None
    is_ok = False

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                message = "Successfully login"
                login(request, user)
                is_ok = True
        else:
            message = "Invalid account data."
    else:
        form = AuthenticationForm()

    for visible in form.visible_fields():
        visible.field.widget.attrs['placeholder'] = 'User ID' if visible.name == 'username' else 'Password'
        visible.field.widget.attrs['class'] = 'form-control'

    return render(request, 'login.html', {'form': form, 'message': message, 'is_ok': is_ok})


def logout_view(request):
    logout(request)
    return redirect("index")