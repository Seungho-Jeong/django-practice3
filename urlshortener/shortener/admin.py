from django.contrib import admin

from .models import PayPlan


@admin.register(PayPlan)
class PayPlanAdmin(admin.ModelAdmin):
    pass
