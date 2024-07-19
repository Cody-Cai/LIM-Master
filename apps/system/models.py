from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import activate, get_language_info, get_language
from django.contrib.auth.models import Permission
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


class EmptyModel(models.Model):
    pass


# Create your models here.
class Language(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Code"))
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Description"))

    def __str__(self):
        return "(%s) %s" % (self.code,self.description)

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


class Menu(models.Model):
    NAVBAR = 'N'
    SIDEBAR = 'S'
    TYPE_CHOICES = [
        (NAVBAR, 'Navbar'),
        (SIDEBAR, 'Sidebar'),
    ]
    name = models.CharField(max_length=30, verbose_name="Name")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Parent Id")
    url = models.CharField(max_length=128, null=True, blank=True)
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="Icon")
    menutype = models.CharField(max_length=2, null=True, blank=True, choices=TYPE_CHOICES, default=SIDEBAR) 
    permission = models.ForeignKey('auth.Permission', on_delete=models.SET_NULL, null=True, blank=True)
    seq = models.FloatField(null=True, blank=True, verbose_name="Order")
    is_home = models.BooleanField(default=False, verbose_name="Home")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["name", "parent"]
        ordering = ["seq"]

    def __str__(self):
        if self.parent:
            return f'{self.parent}|{self.name}'
        else:
            return self.name

    def menu_perms(self):
        """Perms for menu on the template."""
        return "%s.%s" % (self.permission.content_type.app_label, self.permission.codename)

    def menutxt(self):
        lang_code = get_language()
        try:
            Lang = Language.objects.get(code=lang_code)
            menu_txt = MenuLangName.objects.get(menuid=self.id, lang=Lang)
            return menu_txt.name
        except ObjectDoesNotExist:
            return self.name
            

class MenuLangName(models.Model):
    menuid = models.ForeignKey('Menu', on_delete=models.CASCADE)
    lang  = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30, verbose_name="Name")

    class Meta:
        unique_together = ["menuid", "lang"]

    def __str__(self):
        return self.name