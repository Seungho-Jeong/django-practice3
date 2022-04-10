from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm
from .models import User


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        message = "올바르지 않은 데이터 입니다."
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "회원가입완료"
        return render(request, "register.html", {"form": form, "msg": message})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})


def login_view(request):
    is_ok = False
    message = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
            message = "올바른 유저ID와 패스워드를 입력하세요."
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                message = "올바른 유저ID와 패스워드를 입력하세요."
            else:
                if user.check_password(raw_password):
                    message = None
                    login(request, user)
                    is_ok = True
                    request.session["remember_me"] = remember_me

                    # if not remember_me:
                    #     request.session.set_expirey(0)
    else:
        msg = None
        form = LoginForm()
    print("REMEMBER_ME: ", request.session.get("remember_me"))
    return render(request, "login.html", {"form": form, "msg": message, "is_ok": is_ok})


def logout_view(request):
    logout(request)
    return redirect("login")
