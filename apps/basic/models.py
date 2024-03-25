from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.system.models import Language


class CountryRegion(models.Model):
    code = models.CharField(max_length=2, unique=True, verbose_name=_('Country/region'))
    name = models.CharField(max_length=250)
    en_name = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('english name'))

    def __str__(self):
        return  "(%s) %s" % (self.code,self.name)


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_('currency'))
    name = models.CharField(max_length=60)
    symbol = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return  self.code


class CompanyInfo(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name=_('company name'))
    en_name = models.CharField(max_length=60, null=True, blank=True, verbose_name=_('english name'))
    taxnum = models.CharField(max_length=18, null=True, blank=True, verbose_name=_('tax number'))
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('address'))
    zipcode = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('zip code'))
    countryregion = models.ForeignKey('CountryRegion', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Country/region'))
    language = models.ForeignKey('system.Language', on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True, blank=True)
    telephone = models.CharField(max_length=40, null=True, blank=True)
    telephoneext = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('extension'))
    teleFax = models.CharField(max_length=40, null=True, blank=True)
    mobilephone = models.CharField(max_length=40, null=True, blank=True, verbose_name="mobile phone")
    email = models.EmailField(null=True, blank=True)
    url = models.URLField(null=True, blank=True, verbose_name="web site")

    def __str__(self):
        return self.name


class CompanyAddress(models.Model):
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

    company =  models.ForeignKey('CompanyInfo', on_delete=models.CASCADE)
    name = models.CharField(max_length=60, unique=True, verbose_name=_('name'))
    addresstype = models.CharField(max_length=2, choices=TYPE_CHOICES, default=NONE, null=True, blank=True, verbose_name=_('address type'))
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('address'))
