from django.forms import ModelForm, TextInput, HiddenInput, Textarea
from django.forms import inlineformset_factory
from .models import ItemTable, ItemTableModule, ItemTxt
from django.utils.translation import gettext_lazy as _


class ItemTableModuleForm(ModelForm):
    class Meta:
        model = ItemTableModule
        fields = ["unit","tax_item_group","overdelivery_pct","underdelivery_pct"]


ItemTxtFormset = inlineformset_factory(
    ItemTable, ItemTxt, fields=["language", "txt"], extra=1, can_delete=True
)