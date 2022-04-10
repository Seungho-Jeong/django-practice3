from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User
from django.shortcuts import render, redirect

from accounts.forms import RegisterForm


def index(request):
    # print(request.user.pay_plan.name)
    print(request.user.is_superuser)
    user = User.objects.filter(id=request.user.id).first()
    email = user.email if user else "Anonymous User!"
    if not request.user.is_authenticated:
        email = "Anonymous User!"
    print(email)
    return render(request, "base.html", {"welcome_msg": "Hello FastCampus!"})


@csrf_exempt
def get_user(request, user_id):
    print(user_id)
    if request.method == "GET":
        abc = request.GET.get("abc")
        xyz = request.GET.get("xyz")
        user = User.objects.filter(pk=user_id).first()
        return render(request, "base.html", {"user": user, "params": [abc, xyz]})
    elif request.method == "POST":
        username = request.GET.get("username")
        if username:
            user = User.objects.filter(pk=user_id).update(username=username)

        return JsonResponse(dict(msg="You just reached with Post Method!"), status=201, safe=False)


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
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        msg = "Invalid account data."

        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)

            if user is not None:
                msg = "Successfully login"
                login(request, user)

        return render(request, "login.html", {"form": form, "msg": msg})

    else:
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("index")


@login_required
def list_view(request):
    page = int(request.GET.get('p', 1))
    users = User.objects.all().order_by('-id')
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)

    return render(request, 'boards.html', {'users': users})
