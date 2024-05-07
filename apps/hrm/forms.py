from django.forms import ModelForm, TextInput, HiddenInput, Textarea
from .models import Employee
from django.utils.translation import gettext_lazy as _


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
        widgets = {
            "contact_address": Textarea(attrs={"rows": 3}),
        }