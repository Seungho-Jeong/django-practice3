from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User
from django.shortcuts import render


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


@login_required
def list_view(request):
    page = int(request.GET.get('p', 1))
    users = User.objects.all().order_by('-id')
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)

    return render(request, 'boards.html', {'users': users})
