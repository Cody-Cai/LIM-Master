from django.db import models
from django.utils.translation import get_language, gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import translation
from django.conf import settings

from basic.models import Unit, Currency, CountryRegion, DlvTerm, DlvMode, DlvDestination
from ledger.models import TaxGroupHeading, PaymTerm
from system.models import Language
from hrm.models import Employee
from utils.common_field import AddressType
from django.urls import reverse


class VendGroup(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Vendor group"))
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Vendor groups")

    def __str__(self):
        return self.code


class VendTable(models.Model):
    account_num = models.CharField(max_length=20, unique=True, verbose_name=_('Account'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    short_name = models.CharField(max_length=60, null=True, blank=True, verbose_name=_('Short name'))
    invoice_account = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Invoice account")
    vend_group = models.ForeignKey(VendGroup, on_delete=models.RESTRICT, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    countryregion = models.ForeignKey(CountryRegion, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Country/region'))
    url = models.URLField(null=True, blank=True, verbose_name="Internet address")
    main_contact = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Main contact"))
    dlv_term = models.ForeignKey(DlvTerm, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Terms of delivery"))
    dlv_mode = models.ForeignKey(DlvMode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Mode of delivery"))
    dlv_destination = models.ForeignKey(DlvDestination, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Destination of delivery"))
    paym_term = models.ForeignKey(PaymTerm, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Terms of payment"))
    tax_group = models.ForeignKey(TaxGroupHeading, on_delete=models.RESTRICT, blank=True, null=True)
    incl_tax = models.BooleanField(_("Prices incl. sales tax"), default=True, help_text=_("Do prices include sales tax?"))
    notes = models.TextField(_("notes"), null=True, blank=True)
    blocked = models.BooleanField(_("Stopped"), default=False, help_text=_("Is the account locked?"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="creater", verbose_name=_("Created by"))
    created_dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created date time"))
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="modifieder", verbose_name=_("Last modified by"))
    lastmodified_dt = models.DateTimeField(auto_now=True, verbose_name=_("Last modified date time"))


    class Meta:
        verbose_name = _("Vendors")

    def __str__(self):
        return f'{self.account_num} | {self.short_name}' 


class VendAddress(models.Model):
    vendtable = models.ForeignKey(VendTable, on_delete=models.CASCADE, verbose_name=_('Vend account'))
    name = models.CharField(max_length=60, verbose_name=_('name'))
    is_primary = models.BooleanField(_("Primary"), help_text=_("Primary address for address book record."))
    addresstype = AddressType()
    address = models.TextField(max_length=250, null=True, blank=True, verbose_name=_('Address'))
    zipcode = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Postal code'))
    city = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('City'))
    state = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('State'))
    countryregion = models.ForeignKey(CountryRegion, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Country/region'))

    class Meta:
        unique_together = ["vendtable", "name"]
        verbose_name = _("Vendor addresses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this address."""
        return reverse('vend:vendaddress-detail', args=[str(self.id)])

    # def clean(self):
    #     data = self.is_primary
    #     print(data)
    #     if data:
    #         raise ValidationError(
    #             {"is_primary": _("You have forgotten about Fred!")}
    #         )

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        

class VendContact(models.Model):
    vendtable = models.ForeignKey(VendTable, on_delete=models.CASCADE, verbose_name=_('Vend account'))
    is_primary = models.BooleanField(_("Primary"))
    name = models.CharField(max_length=60, unique=True, verbose_name=_('Contact'))
    telephone = models.CharField(max_length=40, null=True, blank=True)
    telephoneext = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Extension'))
    teleFax = models.CharField(max_length=40, null=True, blank=True, verbose_name=_("Fax"))
    mobilephone = models.CharField(max_length=40, null=True, blank=True, verbose_name=_("Mobile phone"))
    email = models.EmailField(null=True, blank=True, verbose_name=_("E-mail"))
    
    class Meta:
        verbose_name = _("Vendor contact")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this address."""
        return reverse('vend:vendcontact-detail', args=[str(self.id)])
    