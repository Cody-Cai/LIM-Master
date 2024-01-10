from django.forms import inlineformset_factory
from .models import Menu, MenuLangName

MenuLangNameFormset = inlineformset_factory(
    Menu, MenuLangName, fields=["lang", "name"], extra=1, can_delete=True
)