from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from apps.basic.models import CountryRegion
from django.conf import settings


class OrganizationUnit(models.Model):
    unitid = models.CharField(verbose_name=_("Organization unit"), max_length=20, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    parentunit = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Parent Organization Unit"))

    def __str__(self):
        return self.unitid


class PersonTitle(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name=_('name'), help_text=_("person title"))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("person title")


class Employee(models.Model):
    NONE = "N"
    MALE = "M"
    FEMALE = "F"
    GENDER = [
        (NONE, _("None")),
        (MALE, _("Male")),
        (FEMALE, _("Female")),
    ]

    EMPLOYED = "M"
    RESIGNED = "F"
    STATUS = [
        (NONE, _("None")),
        (EMPLOYED, _("Employed")),
        (RESIGNED, _("Resigned")),
    ]

    MARRIED = "M"
    SINGLE = "S"
    WIDOWED = "W"
    DIVORCED = "D"
    MARITAL_STATUS = [
        (NONE, _("None")),
        (MARRIED, _("Married")),
        (SINGLE, _("Single")),
        (WIDOWED, _("Widowed")),
        (DIVORCED, _("Divorced")),
    ]

    OFFICIAL = 'O'
    PROBATION = 'P'
    TEMPORARY = 'T'

    TYPE_CHOICES = [
        (OFFICIAL, _("Official")),
        (PROBATION, _("Probation")),
        (TEMPORARY, _("Temporary")),
    ]

    emplid = models.CharField(max_length=20, unique=True, verbose_name=_("employee"), help_text=_("employee number"))
    name = models.CharField(max_length=60, verbose_name=_("name"), help_text=_("employee name"))
    orgnization_unit = models.ForeignKey(OrganizationUnit, on_delete=models.RESTRICT, null=True, blank=True)
    title = models.ForeignKey(PersonTitle, on_delete=models.RESTRICT, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, null=True, blank=True)
    employee_type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True, blank=True)
    seniority_date = models.DateField(null=True, blank=True)
    probation_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    id_number = models.CharField(max_length=18, null=True, blank=True, verbose_name=_("ID number"))
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS, null=True, blank=True)
    education = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    contact_address = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('contact address'))
    countryregion = models.ForeignKey('basic.CountryRegion', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Country/region'))
    emergency_contact = models.CharField(max_length=60, verbose_name=_("name"), null=True, blank=True, help_text=_("emergency contact"))
    emergency_number = models.CharField(max_length=40, null=True, blank=True)
    notes = models.TextField(_("notes"), null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["emplid"]

    def __str__(self):
        return f'{self.emplid}, {self.name}'

    def get_absolute_url(self):
        return reverse("employee-detail", kwargs={"pk": self.pk})
    
    #JSON
    def get_data(self):
        return {
            'id': self.id,
            'emplid': self.emplid,
            'name': self.name,
            'title': self.title.name,
            'orgnization': self.orgnization_unit.unitid,
            'status': self.get_status_display()
        }