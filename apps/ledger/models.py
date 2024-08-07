from django.db import models
from django.utils.translation import gettext_lazy as _
from basic.models import Currency
# Create your models here.


class TaxTable(models.Model):
    HALF_UP = "O"
    UP = "U"
    DOWN = "D"
    ROUND_CHOICES = [
        (HALF_UP, _('round off')),
        (UP, _('up')),
        (DOWN, _('down')),
    ]

    code = models.CharField(max_length=10, unique=True, verbose_name=_("Tax code"))
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Name"))
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    roundoff = models.FloatField(_("Round-off"), default=0.01, help_text=_('Special rounding-off for VAT'))
    roundoff_type =  models.CharField(max_length=2, choices=ROUND_CHOICES, default=HALF_UP, verbose_name=_('Rounding form'))
    value = models.FloatField(help_text=_('Percentage or amount per unit'))

    class Meta:
        verbose_name = _("VAT codes")

    def __str__(self):
        return self.code

    #JSON
    def get_data(self):
        str_cur = '' if self.currency is None else self.currency.code

        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'currency': str_cur,
            'roundoff': self.roundoff,
            'roundoff_type': self.get_roundoff_type_display(),
            'value': self.value
        }
    


class TaxGroupHeading(models.Model):
    tax_group = models.CharField(max_length=10, unique=True, verbose_name=_("Tax group"))
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Name"))
    tax_code = models.ManyToManyField(TaxTable)

    class Meta:
        verbose_name = _("Tax group")

    def __str__(self):
        return self.tax_group

    def display_tax(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(tax_code.code for tax_code in self.tax_code.all()[:3])

    display_tax.short_description = 'Tax'

    #JSON
    def get_data(self):
        return {
            'id': self.id,
            'tax_group': self.tax_group,
            'name': self.name,
            'display_tax': self.display_tax(),
        }


class TaxItemGroupHeading(models.Model):
    tax_item_group = models.CharField(max_length=10, unique=True, verbose_name=_("Item tax group"))
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Name"))
    tax_code = models.ManyToManyField(TaxTable)

    class Meta:
        verbose_name = _("Item tax group")

    def __str__(self):
        return self.tax_item_group

    def display_tax(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(tax_code.code for tax_code in self.tax_code.all()[:3])

    display_tax.short_description = 'Tax'

    #JSON
    def get_data(self):
        return {
            'id': self.id,
            'tax_item_group': self.tax_item_group,
            'name': self.name,
            'display_tax': self.display_tax(),
        }


""" PaymTerm """
class PaymTerm(models.Model):
    NET = "N"
    MONTH = "M"
    QUART = "Q"
    YEAR = "Y"
    WEEK = "Y"
    COD = "C"
    METHOD_CHOICES = [
        (NET, _('Net')),
        (MONTH, _('Curr.Mth.')),
        (QUART, _('Curr.Qtr.')),
        (YEAR, _('Curr.Year')),
        (WEEK, _('Curr.Week')),
        (COD, _('C.O.D.')),
    ]

    code = models.CharField(max_length=10, unique=True, verbose_name=_("Payment terms"))
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    paym_method =  models.CharField(max_length=2, choices=METHOD_CHOICES, default=NET, verbose_name=_('Payment method'))
    num_of_months = models.PositiveSmallIntegerField(_("Months"), default=0, help_text=_("Number of months past the specified method of payment")) 
    num_of_weeks = models.PositiveSmallIntegerField(_("Weeks"), default=0, help_text=_("Number of weeks past the specified method of payment"))
    num_of_days = models.PositiveSmallIntegerField(_("Days"), default=0, help_text=_("Number of days past the specified method of payment")) 


    class Meta:
        verbose_name = _("Terms of payment")

    def __str__(self):
        return self.code

    #JSON
    def get_data(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'paym_method': self.get_paym_method_display(),
            'num_of_months': self.num_of_months,
            'num_of_weeks': self.num_of_weeks,
            'num_of_days': self.num_of_days,
        }