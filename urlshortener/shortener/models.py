import random
import string

from django.db import models

from accountapp.models import User


class PayPlan(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ShortenedUrls(models.Model):
    class UrlCreatedVia(models.TextChoices):
        WEBSITE = 'web'
        TELEGRAM = 'telegram'

    def random_string():
        str_pool = string.digits + string.ascii_letters
        return ("".join([random.choice(str_pool) for _ in range(6)])).lower()

    nick_name = models.CharField(max_length=100)
    target_url = models.CharField(max_length=2000)
    shortened_url = models.CharField(max_length=6, default=random_string())
    created_via = models.CharField(max_length=8, choices=UrlCreatedVia.choices, default=UrlCreatedVia.WEBSITE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
