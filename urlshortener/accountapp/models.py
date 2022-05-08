from django.contrib.auth.models import AbstractUser
from django.db import models

from shortener.models import PayPlan


class User(AbstractUser):
    pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING, null=True)
    full_name = models.CharField(max_length=100)
