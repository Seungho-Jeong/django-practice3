from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User
from django.shortcuts import render

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
