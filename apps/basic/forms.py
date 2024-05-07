from django.forms import ModelForm, TextInput, HiddenInput, Textarea
from django.forms import inlineformset_factory
from .models import CompanyInfo, CompanyAddress, UnitTxt, Unit
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


UnitTxtFormset = inlineformset_factory(
    Unit, UnitTxt, fields=["language", "unitid_txt"], extra=1, can_delete=True
)