from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class ItemGroup(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Item group"))
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Item group")

    def __str__(self):
        return self.code


class ItemConfig(models.Model):
    config = models.CharField(max_length=20, unique=True, verbose_name=_("Config"))
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Item config")

    def __str__(self):
        return self.config


class ItemColor(models.Model):
    color = models.CharField(max_length=20, unique=True, verbose_name=_("Color"))
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Item color")

    def __str__(self):
        return self.color


class ItemSize(models.Model):
    size = models.CharField(max_length=20, unique=True, verbose_name=_("Size"))
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Item size")

    def __str__(self):
        return self.size


class InventSite(models.Model):
    site = models.CharField(max_length=20, unique=True, verbose_name=_("Site"))
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Site")

    def __str__(self):
        return self.site


class InventLocation(models.Model):
    location = models.CharField(max_length=20, unique=True, verbose_name=_("Site"))
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Name"))
    site = models.ForeignKey(InventSite, on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        verbose_name = _("Site")

    def __str__(self):
        return self.site