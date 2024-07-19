from django.db import models
from django.utils.translation import get_language, gettext_lazy as _
from basic.models import Unit
from ledger.models import TaxItemGroupHeading
from system.models import Language
from django.core.exceptions import ObjectDoesNotExist
from django.utils import translation


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


class InventWarehouse(models.Model):
    warehouse = models.CharField(max_length=20, unique=True, verbose_name=_("Warehouses"))
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Name"))
    site = models.ForeignKey(InventSite, on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        unique_together = ["warehouse", "site"]
        verbose_name = _("Warehouses")

    def __str__(self):
        return self.warehouse


class InventAisle(models.Model):
    aisle = models.CharField(max_length=20, verbose_name=_("Aisle"))
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Name"))
    warehouse = models.ForeignKey(InventWarehouse, on_delete=models.RESTRICT)

    class Meta:
        unique_together = ["warehouse", "aisle"]
        verbose_name = _("Aisle")

    def __str__(self):
        return f'{self.warehouse} | {self.aisle}'


class InventLocation(models.Model):
    location = models.CharField(max_length=20, verbose_name=_("Locations"))
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Name"))
    warehouse = models.ForeignKey(InventWarehouse, on_delete=models.RESTRICT)
    aisle = models.ForeignKey(InventAisle, on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        unique_together = ["location", "warehouse"]
        verbose_name = _("Locations")

    def __str__(self):
        return self.location


class ItemTable(models.Model):
    ITEM = "I"
    SERVICE = "S"
    TYPE_CHOICES = [
        (ITEM, _('item')),
        (SERVICE, _('service')),
    ]

    item_id = models.CharField(max_length=20, unique=True, verbose_name=_("Item number"))
    item_name = models.CharField(max_length=60, verbose_name=_("Item name"))
    item_group = models.ForeignKey(ItemGroup, on_delete=models.RESTRICT, verbose_name=_("Item group"))
    item_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=ITEM, verbose_name=_('Item type'))
    standard_config = models.ForeignKey(ItemConfig, on_delete=models.RESTRICT, null=True, blank=True, verbose_name=_("config"))
    standard_size = models.ForeignKey(ItemSize, on_delete=models.RESTRICT, null=True, blank=True, verbose_name=_("size"))
    standard_color = models.ForeignKey(ItemColor, on_delete=models.RESTRICT, null=True, blank=True, verbose_name=_("color"))

    class Meta:
        verbose_name = _("Items")

    def __str__(self):
        return f'{self.item_id}({self.item_name})' 

    def default_txt(self):
        cur_language = translation.get_language()
        #print(cur_language)
        language = Language.objects.get(code=cur_language)
        
        try:
            item_txt = ItemTxt.objects.get(item=self.id,language=language)
            return item_txt.txt
        except ObjectDoesNotExist:
            return ""

    #JSON
    def get_data(self):
        str_conf = '' if self.standard_config is None else self.standard_config.config
        str_color = '' if self.standard_color is None else self.standard_color.color
        str_size = '' if self.standard_size is None else self.standard_size.size

        return {
            'id': self.id,
            'item_id': self.item_id,
            'item_name': self.item_name,
            'item_group': self.item_group.code,
            'item_type': self.get_item_type_display(),
            'standard_config': str_conf, 
            'standard_size': str_size,
            'standard_color': str_color,
        }


class ItemTxt(models.Model):
    item  = models.ForeignKey(ItemTable, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    txt = models.TextField(_("text"), max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ["item", "language"]
        verbose_name = _("item texts")
    
    def __str__(self):
        return  self.txt


class ItemTableModule(models.Model):
    INVENT = "I"
    PURCH = "P"
    SALES = "S"
    TYPE_CHOICES = [
        (INVENT, _('inventory')),
        (PURCH, _('purchase')),
        (SALES, _('sales')),
    ]

    item  = models.ForeignKey(ItemTable, on_delete=models.CASCADE)
    module_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name=_('Module type'))
    unit = models.ForeignKey(Unit, on_delete=models.RESTRICT, blank=True, null=True)
    tax_item_group = models.ForeignKey(TaxItemGroupHeading, on_delete=models.RESTRICT, blank=True, null=True)
    overdelivery_pct = models.FloatField(_("Overdelivery"), default=0, help_text=_("Accepted overdelivery in percentage"))
    underdelivery_pct = models.FloatField(_("Underdelivery"), default=0, help_text=_("Accepted underdelivery in percentage"))

    class Meta:
        unique_together = ["item", "module_type"]
        verbose_name = _("Inventory module parameters")

    def __str__(self):
        return f'{self.get_module_type_display()} {self.unit}'


class InventBatch(models.Model):
    batch_id = models.CharField(max_length=20, verbose_name=_("Batch number"))
    item  = models.ForeignKey(ItemTable, on_delete=models.CASCADE)
    exp_date = models.DateField(verbose_name=_("Expiry date"))
    prod_date = models.DateField(verbose_name=_("Manufacturing date"))
    description = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = ["item", "batch_id"]
        verbose_name = _("Batches")

    def __str__(self):
        return self.batch_id


class InventDim(models.Model):
    batch  = models.ForeignKey(InventBatch, on_delete=models.RESTRICT, null=True, blank=True)
    site  = models.ForeignKey(InventSite, on_delete=models.RESTRICT, null=True, blank=True)
    warehouse  = models.ForeignKey(InventWarehouse, on_delete=models.RESTRICT, null=True, blank=True)
    location  = models.ForeignKey(InventLocation, on_delete=models.RESTRICT, null=True, blank=True)
    config = models.ForeignKey(ItemConfig, on_delete=models.RESTRICT, null=True, blank=True, verbose_name=_("config"))
    size = models.ForeignKey(ItemSize, on_delete=models.RESTRICT, null=True, blank=True, verbose_name=_("size"))
    color = models.ForeignKey(ItemColor, on_delete=models.RESTRICT, null=True, blank=True, verbose_name=_("color"))

    class Meta:
        unique_together = ["batch","site","warehouse","location","config","size","color"]
        verbose_name = _("Inventory dimensions")

    def __str__(self):
        return self.id


class InventSum(models.Model):
    item  = models.ForeignKey(ItemTable, on_delete=models.RESTRICT)
    inventdim = models.ForeignKey(InventDim, on_delete=models.RESTRICT)
    post_qty =  models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Posted quantity"), help_text=_("Financially entered quantity"))
    post_value =  models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Financial cost amount"), help_text=_("Inventory value for the financially updated quantity."))
    deducted = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Deducted"), help_text=_("Quantity that has been physically deducted, but not posted."))
    received = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Received"), help_text=_("Physical quantity received, but not posted"))
    reserv_physical = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Physical reserved"), help_text=_("Quantity reserved of the physical quantity"))
    reserv_ordered = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Ordered reserved"), help_text=_("Quantity reserved on quantity ordered"))
    onorder = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("On order"), help_text=_("Quantity on order"))
    ordered = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Ordered"), help_text=_("Quantity ordered"))
    closed = models.BooleanField(_("Closed"), help_text=_("Is the on-hand inventory closed, that is with no quantity and value?"))

    class Meta:
        unique_together = ["item","inventdim"]
        verbose_name = _("On-hand inventory")

    def __str__(self):
        return self.id
