from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import UrlCreateForm
from .models import ShortenedUrls
from account.models import User


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


def url_list(request):
    get_list = ShortenedUrls.objects.order_by("-created_at").all()
    return render(request, 'url_list.html', {'list': get_list})


@login_required()
def url_create(request):
    message = None
    if request == 'POST':
        form = UrlCreateForm(request.POST)
        if form.is_valid():
            message = f"{form.cleaned_data.get('nick_name')} created!"
            messages.add_message(request, messages.INFO, message)
            form.save(request)
            return redirect('url_list')
        else:
            form = UrlCreateForm()
    else:
        form = UrlCreateForm()
    return render(request, 'url_create.html', {'form': form})


@login_required()
def url_change(request, action, url_id):
    if request.method == 'POST':
        url_data = ShortenedUrls.objects.filter(id=url_id)
        if url_data.exists():
            if url_data.first().created_by_id != request.user.id:
                message = 'Forbidden'
            else:
                if action == 'delete':
                    message = f"{url_data.first().nick_name} deleted!"
                    url_data.delete()
                    messages.add_message(request, messages.INFO, message)
                elif action == 'update':
                    message = f"{url_data.first().nick_name} updated!"
                    form = UrlCreateForm(request.POST)
                    form.update_form(request, url_id)
                    messages.add_message(request, messages.INFO, message)
        else:
            message = 'Does not exist url.'
    elif request.method == 'GET' and action == 'update':
        url_data = ShortenedUrls.objects.filter(id=url_id).first()
        form = UrlCreateForm(instance=url_data)
        return render(request, 'url_create.html', {'form': form, 'is_update': True})

    return redirect('url_list')