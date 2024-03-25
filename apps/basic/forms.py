from django.forms import ModelForm, TextInput, HiddenInput, Textarea
from .models import CompanyInfo, CompanyAddress
from django.utils.translation import gettext_lazy as _


class CompanyForm(ModelForm):
    class Meta:
        model = CompanyInfo
        fields = "__all__"
        widgets = {
            "address": Textarea(attrs={"rows": 3}),
        }


class CompanyAddressForm(ModelForm):
    class Meta:
        model = CompanyAddress
        fields = ["name","addresstype","address"]
        widgets = {
            "address": Textarea(attrs={"rows": 3}),
        }