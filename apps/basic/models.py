from django.db import models
from django.utils.translation import get_language, gettext_lazy as _
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("person title")
    

class Unit(models.Model):
    unit_id = models.CharField(max_length=5, unique=True, verbose_name=_("unit"))
    txt = models.CharField(_("name"), max_length=30, blank=True)
    unit_decimals = models.PositiveSmallIntegerField(_("decimals"), default=2)
    symbol = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        verbose_name = _("units")

    
    def __str__(self):
        return  self.unit_id

    
    def language_unit(self, unitid, languageid=get_language()):
        language = Language.objects.get(code=languageid)
        
        try:
            unit_txt = UnitTxt.objects.get(unit=self.id,language=language)
            return unit_txt.unitid_txt
        except ObjectDoesNotExist:
            return unitid


class UnitTxt(models.Model):
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE)
    language = models.ForeignKey('system.Language', on_delete=models.SET_NULL, null=True, blank=True)
    unitid_txt = models.CharField(_("text"), max_length=10, blank=True)

    class Meta:
        verbose_name = _("unit texts")
        unique_together = ["unit", "language"]
    
    def __str__(self):
        return  self.unitid_txt


class UnitConvert(models.Model):
    HALF_UP = "O"
    UP = "U"
    DOWN = "D"
    ROUND_CHOICES = [
        (HALF_UP, _('round off')),
        (UP, _('up')),
        (DOWN, _('down')),
    ]

    from_unit = models.ForeignKey("Unit", on_delete=models.RESTRICT, blank=True, verbose_name=_("from unit"), related_name="from_unit")
    to_unit = models.ForeignKey("Unit",  on_delete=models.RESTRICT, blank=True, verbose_name=_("to unit"), related_name="to_unit")
    factor = models.DecimalField(max_digits=9, decimal_places=5)
    markup = models.DecimalField(_("additional quantity"), default=0, max_digits=5, decimal_places=2)
    round_off =  models.CharField(max_length=2, choices=ROUND_CHOICES, default=HALF_UP, verbose_name=_('round-off'))

    class Meta:
        verbose_name = _("unit conversion")
        unique_together = ["from_unit", "to_unit"]

    def __str__(self):
        return  self.from_unit.unit_id

     #JSON
    def get_data(self):
        return {
            'id': self.id,
            'from_unit': self.from_unit.unit_id,
            'to_unit': self.to_unit.unit_id,
            'factor': self.factor,
            'markup': self.markup,
            'round_off': self.get_round_off_display()
        }


class NumberSequenceTable(models.Model):
    number_code = models.CharField(_("number sequence code"), max_length=10, unique=True)
    txt = models.CharField(_("name"), max_length=30, blank=True)
    lowest = models.PositiveIntegerField(_("smallest"), default=1)
    highest = models.PositiveIntegerField(_("largest"))
    next_rec = models.PositiveIntegerField(_("next"), blank=True)
    num_format = models.CharField(_("format"), max_length=30, blank=True)


    class Meta:
        verbose_name = _("number sequence")

    def __str__(self):
        return self.number_code