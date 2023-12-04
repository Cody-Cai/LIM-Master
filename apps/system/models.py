from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import activate, get_language_info

# Create your models here.
class Language(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Code"))
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Description"))

    def __str__(self):
        return self.code

    def display_name(self):
        li = get_language_info(self.code)
        return  f'{li["name_local"]}'

    #JSON
    def get_data(self):
        return {
            'id': self.id,
            'code': self.code,
            'description': self.description,
        }