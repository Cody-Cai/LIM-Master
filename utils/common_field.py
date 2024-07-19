from django.db import models
from django.utils.translation import get_language, gettext_lazy as _


class AddressType(models.CharField):
    NONE = "N"
    DELIVERY = "D"
    INVOICE = "I"
    PAYMENT = "P"
    OTHER = "O"
    TYPE_CHOICES = [
        (NONE, _('none')),
        (DELIVERY, _('delivery')),
        (INVOICE, _('invoice')),
        (PAYMENT, _('payment')),
        (OTHER, _('other')),
    ]

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 2
        kwargs["choices"] = self.TYPE_CHOICES
        kwargs["default"] = self.NONE
        kwargs["verbose_name"] = _('address type')
        super().__init__(*args, **kwargs)