from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ShortenedUrls


class UrlCreateForm(forms.ModelForm):
    class Meta:
        model = ShortenedUrls
        fields = ["nick_name", "target_url"]
        labels = {
            "nick_name": _("별칭"),
            "target_url": _("URL"),
        }
        widgets = {
            "nick_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "URL을 구분하기 위한 별칭"}),
            "target_url": forms.TextInput(attrs={"class": "form-control", "placeholder": "포워딩될 URL"}),
        }

    def save(self, request, commit=True):
        instance = super(UrlCreateForm, self).save(commit=False)
        instance.target_url = instance.target_url.strip()
        instance.created_by = request.user.id
        if commit:
            instance.save()
        return instance

    def update_form(self, request, url_id):
        instance = super(UrlCreateForm, self).save(commit=False)
        instance.target_url = instance.target_url.strip()
        ShortenedUrls.objects.filter(
            pk=url_id,
            created_by_id=request.user.id
        ).update(
            target_url=instance.target_url,
            nick_name=instance.nick_name
        )
