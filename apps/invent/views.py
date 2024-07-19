from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView
from django.http import JsonResponse, HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils import translation
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import messages
from .models import ItemGroup, ItemColor, ItemConfig, ItemSize, InventSite, InventWarehouse, InventAisle, InventLocation, ItemTable, ItemTableModule, ItemTxt, InventBatch
from utils import custom
from .forms import ItemTableModuleForm

import json


class ItemGroupListView(PermissionRequiredMixin, generic.ListView):
    model = ItemGroup
    template_name = "invent/itemgroup_list.html"
    permission_required = "invent.view_itemgroup"


class ItemGroup_Json(custom.JSONResponseMixin):
    permission_required = "invent.view_itemgroup"

    def get_data(self, context):
        fields = ['id','code','name']
        ret = dict(data=list(ItemGroup.objects.values(*fields)))
        return super().get_data(ret)


class ItemGroupCreateView(custom.ObjectCreateView):
    model = ItemGroup
    fields = '__all__'
    success_url = reverse_lazy('invent:itemgroup')
    permission_required = "invent.add_itemgroup"
    title = model._meta.verbose_name


class ItemGroupUpdateView(custom.ObjectUpdateView):
    model = ItemGroup
    fields = ['code','name']
    success_url = reverse_lazy('invent:itemgroup')
    permission_required = "invent.change_itemgroup"
    title = model._meta.verbose_name


class ItemGroupDeleteView(custom.ObjectDeleteView):
    model = ItemGroup
    success_url = reverse_lazy('invent:itemgroup')
    permission_required = "invent.delete_itemgroup"
    title = model._meta.verbose_name


class ItemConfigListView(PermissionRequiredMixin, generic.ListView):
    model = ItemConfig
    template_name = "invent/itemconfig_list.html"
    permission_required = "invent.view_itemconfig"


class ItemConfig_Json(custom.JSONResponseMixin):
    permission_required = "invent.view_itemconfig"

    def get_data(self, context):
        fields = ['id','config','description']
        ret = dict(data=list(ItemConfig.objects.values(*fields)))
        return super().get_data(ret)


class ItemConfigCreateView(custom.ObjectCreateView):
    model = ItemConfig
    fields = '__all__'
    success_url = reverse_lazy('invent:itemconfig')
    permission_required = "invent.add_itemconfig"
    title = model._meta.verbose_name


class ItemConfigUpdateView(custom.ObjectUpdateView):
    model = ItemConfig
    fields = ['config','description']
    success_url = reverse_lazy('invent:itemconfig')
    permission_required = "invent.change_itemconfig"
    title = model._meta.verbose_name


class ItemConfigDeleteView(custom.ObjectDeleteView):
    model = ItemConfig
    success_url = reverse_lazy('invent:itemconfig')
    permission_required = "invent.delete_itemconfig"
    title = model._meta.verbose_name


class ItemColorListView(PermissionRequiredMixin, generic.ListView):
    model = ItemColor
    template_name = "invent/itemcolor_list.html"
    permission_required = "invent.view_itemcolor"


class ItemColor_Json(custom.JSONResponseMixin):
    permission_required = "invent.view_itemcolor"

    def get_data(self, context):
        fields = ['id','color','description']
        ret = dict(data=list(ItemColor.objects.values(*fields)))
        return super().get_data(ret)


class ItemColorCreateView(custom.ObjectCreateView):
    model = ItemColor
    fields = '__all__'
    success_url = reverse_lazy('invent:itemcolor')
    permission_required = "invent.add_itemcolor"
    title = model._meta.verbose_name


class ItemColorUpdateView(custom.ObjectUpdateView):
    model = ItemColor
    fields = ['color','description']
    success_url = reverse_lazy('invent:itemcolor')
    permission_required = "invent.change_itemcolor"
    title = model._meta.verbose_name


class ItemColorDeleteView(custom.ObjectDeleteView):
    model = ItemColor
    success_url = reverse_lazy('invent:itemcolor')
    permission_required = "invent.delete_itemcolor"
    title = model._meta.verbose_name


class ItemSizeListView(PermissionRequiredMixin, generic.ListView):
    model = ItemSize
    template_name = "invent/itemsize_list.html"
    permission_required = "invent.view_itemsize"


class ItemSize_Json(custom.JSONResponseMixin):
    permission_required = "invent.view_itemsize"

    def get_data(self, context):
        fields = ['id','size','description']
        ret = dict(data=list(ItemSize.objects.values(*fields)))
        return super().get_data(ret)


class ItemSizeCreateView(custom.ObjectCreateView):
    model = ItemSize
    fields = '__all__'
    success_url = reverse_lazy('invent:itemsize')
    permission_required = "invent.add_itemsize"
    title = model._meta.verbose_name


class ItemSizeUpdateView(custom.ObjectUpdateView):
    model = ItemSize
    fields = ['size','description']
    success_url = reverse_lazy('invent:itemsize')
    permission_required = "invent.change_itemsize"
    title = model._meta.verbose_name


class ItemSizeDeleteView(custom.ObjectDeleteView):
    model = ItemSize
    success_url = reverse_lazy('invent:itemsize')
    permission_required = "invent.delete_itemsize"
    title = model._meta.verbose_name


class InventSiteListView(PermissionRequiredMixin, generic.ListView):
    model = InventSite
    template_name = "invent/inventsite_list.html"
    permission_required = "invent.view_inventsite"


class InventSite_Json(custom.JSONResponseMixin):
    permission_required = "invent.view_inventsite"

    def get_data(self, context):
        fields = ['id','site','name']
        ret = dict(data=list(InventSite.objects.values(*fields)))
        return super().get_data(ret)


class InventSiteCreateView(custom.ObjectCreateView):
    model = InventSite
    fields = '__all__'
    success_url = reverse_lazy('invent:inventsite')
    permission_required = "invent.add_inventsite"
    title = model._meta.verbose_name


class InventSiteUpdateView(custom.ObjectUpdateView):
    model = InventSite
    fields = ['site','name']
    success_url = reverse_lazy('invent:inventsite')
    permission_required = "invent.change_inventsite"
    title = model._meta.verbose_name


class InventSiteDeleteView(custom.ObjectDeleteView):
    model = InventSite
    success_url = reverse_lazy('invent:inventsite')
    permission_required = "invent.delete_inventsite"
    title = model._meta.verbose_name


class InventWarehouseListView(PermissionRequiredMixin, generic.ListView):
    model = InventWarehouse
    template_name = "invent/inventwarehouse_list.html"
    permission_required = "invent.view_inventwarehouse"


class InventWarehouse_Json(custom.JSONResponseMixin):
    permission_required = "invent.view_inventwarehouse"

    def get_data(self, context):
        fields = ['id','warehouse','name','site__site']
        ret = dict(data=list(InventWarehouse.objects.values(*fields)))
        return super().get_data(ret)


class InventWarehouseCreateView(custom.ObjectCreateView):
    model = InventWarehouse
    fields = '__all__'
    success_url = reverse_lazy('invent:inventwarehouse')
    permission_required = "invent.add_inventwarehouse"
    title = model._meta.verbose_name


class InventWarehouseUpdateView(custom.ObjectUpdateView):
    model = InventWarehouse
    fields = ['warehouse','name','site']
    success_url = reverse_lazy('invent:inventwarehouse')
    permission_required = "invent.change_inventwarehouse"
    title = model._meta.verbose_name


class InventWarehouseDeleteView(custom.ObjectDeleteView):
    model = InventWarehouse
    success_url = reverse_lazy('invent:inventwarehouse')
    permission_required = "invent.delete_inventwarehouse"
    title = model._meta.verbose_name


class InventAisleListView(PermissionRequiredMixin, generic.ListView):
    model = InventAisle
    template_name = "invent/inventaisle_list.html"
    permission_required = "invent.view_inventaisle"


class InventAisle_Json(custom.JSONResponseMixin):
    permission_required = "invent.view_inventaisle"

    def get_data(self, context):
        fields = ['id','warehouse__warehouse','name','aisle']
        ret = dict(data=list(InventAisle.objects.values(*fields)))
        return super().get_data(ret)


class InventAisleCreateView(custom.ObjectCreateView):
    model = InventAisle
    fields =  ['id','warehouse','aisle','name']
    success_url = reverse_lazy('invent:inventaisle')
    permission_required = "invent.add_inventaisle"
    title = model._meta.verbose_name


class InventAisleUpdateView(custom.ObjectUpdateView):
    model = InventAisle
    fields = ['warehouse','aisle','name']
    success_url = reverse_lazy('invent:inventaisle')
    permission_required = "invent.change_inventaisle"
    title = model._meta.verbose_name


class InventAisleDeleteView(custom.ObjectDeleteView):
    model = InventAisle
    success_url = reverse_lazy('invent:inventaisle')
    permission_required = "invent.delete_inventaisle"
    title = model._meta.verbose_name


class InventLocationListView(PermissionRequiredMixin, generic.ListView):
    model = InventLocation
    template_name = "invent/inventlocation_list.html"
    permission_required = "invent.view_inventlocation"


class InventLocation_Json(custom.JSONResponseMixin):
    permission_required = "invent.view_inventlocation"

    def get_data(self, context):
        fields = ['id','warehouse__warehouse','location','aisle__aisle']
        ret = dict(data=list(InventLocation.objects.values(*fields)))
        return super().get_data(ret)


class InventLocationCreateView(custom.ObjectCreateView):
    model = InventLocation
    fields =  ['id','warehouse','location','aisle']
    success_url = reverse_lazy('invent:inventlocation')
    permission_required = "invent.add_inventlocation"
    title = model._meta.verbose_name


class InventLocationUpdateView(custom.ObjectUpdateView):
    model = InventLocation
    fields = ['warehouse','location','aisle']
    success_url = reverse_lazy('invent:inventlocation')
    permission_required = "invent.change_inventlocation"
    title = model._meta.verbose_name


class InventLocationDeleteView(custom.ObjectDeleteView):
    model = InventLocation
    success_url = reverse_lazy('invent:inventlocation')
    permission_required = "invent.delete_inventlocation"
    title = model._meta.verbose_name


class ItemTableListView(PermissionRequiredMixin, generic.ListView):
    model = ItemTable
    template_name = "invent/itemtable_list.html"
    permission_required = "invent.view_itemtable"


class ItemTable_Json(PermissionRequiredMixin, View):
    permission_required = "invent.view_itemtable"

    def get(self, request):
        itemtable = ItemTable.objects.all()
        data = [d.get_data() for d in itemtable]
        ret = {'data': data}
        return JsonResponse(ret, safe=False)
        


class ItemTableCreateView(custom.ObjectCreateView):
    model = ItemTable
    fields = ['id','item_id','item_name','item_type','item_group','standard_config','standard_color','standard_size']
    success_url = reverse_lazy('invent:itemtable')
    permission_required = "invent.add_itemtable"
    title = model._meta.verbose_name

    def save_action(self):
        """Create itemtableModule."""
        form = self.get_form()
        # invent = ItemTableModule(item=form.instance, module_type = "I")
        # invent.save()
        # create ItemTableModule object
        ItemTableModule.objects.get_or_create(item=form.instance, module_type = "I")
        ItemTableModule.objects.get_or_create(item=form.instance, module_type = "P")
        ItemTableModule.objects.get_or_create(item=form.instance, module_type = "S")

    def form_valid(self, form): 
        return super().form_valid(form)


class ItemTableUpdateView(custom.ObjectUpdateView):
    model = ItemTable
    fields = ['id','item_id','item_name','item_type','item_group','standard_config','standard_color','standard_size']
    template_name = "invent/itemtable_update.html"
    success_url = reverse_lazy('invent:itemtable')
    permission_required = "invent.change_itemtable"
    title = model._meta.verbose_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invent = ItemTableModule.objects.get(item=self.object, module_type = "I")
        purchase = ItemTableModule.objects.get(item=self.object, module_type = "P")
        sales = ItemTableModule.objects.get(item=self.object, module_type = "S")
        if self.request.method == 'POST':
            inventModuleForm = ItemTableModuleForm(self.request.POST, instance=invent, prefix='inventModuleForm')
            purModuleForm = ItemTableModuleForm(self.request.POST, instance=purchase, prefix='purModuleForm')
            salesModuleForm = ItemTableModuleForm(self.request.POST, instance=sales, prefix='salesModuleForm')
        else:
            inventModuleForm = ItemTableModuleForm(instance=invent, prefix='inventModuleForm')
            purModuleForm = ItemTableModuleForm(instance=purchase, prefix='purModuleForm')
            salesModuleForm = ItemTableModuleForm(instance=sales, prefix='salesModuleForm')
            
        context["inventModuleForm"] = inventModuleForm
        context["purModuleForm"] = purModuleForm
        context["salesModuleForm"] = salesModuleForm

        return context

    def form_valid(self, form):
        item = form.save()
        context = self.get_context_data()
        invetModule = context['inventModuleForm'].save()
        purchaseModule = context['purModuleForm'].save()
        salesModule = context['salesModuleForm'].save()
        return super().form_valid(form)


class ItemTableDeleteView(custom.ObjectDeleteView):
    model = ItemTable
    success_url = reverse_lazy('invent:itemtable')
    permission_required = "invent.delete_itemtable"
    title = model._meta.verbose_name


from .forms import ItemTxtFormset
def manage_itemtxt(request, pk):
    # author = get_object_or_404(Author, pk=pk)
    itemtable = ItemTable.objects.get(pk=pk)
    title = itemtable._meta.verbose_name
    #BookInlineFormSet = inlineformset_factory(Author, Book, fields=('title','genre','language',),can_delete=True)
    if request.method == "POST":
        formset = ItemTxtFormset(request.POST, request.FILES, instance=itemtable)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            #return HttpResponseRedirect(reverse_lazy('system:menu'))
            msg = _("%(title)s %(name)s updated") % {"title": title, "name": itemtable}
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "reloadTable": None,
                        "showMessage": f'{msg}'
                    })
                })
    else:
        formset = ItemTxtFormset(instance=itemtable)

    return render(request, 'invent/itemtxt_form.html', {
        'formset': formset, 
        'object': itemtable,
        'title': title})

    
class InventBatchListView(PermissionRequiredMixin, generic.ListView):
    model = InventBatch
    template_name = "invent/inventbatch_list.html"
    permission_required = "invent.view_inventbatch"


class InventBatch_Json(custom.JSONResponseMixin):
    permission_required = "invent.view_inventbatch"

    def get_data(self, context):
        fields = ['id','batch_id','item__item_id','item__item_name','exp_date','prod_date']
        ret = dict(data=list(InventBatch.objects.values(*fields)))
        return super().get_data(ret)


class InventBatchCreateView(custom.ObjectCreateView):
    model = InventBatch
    fields =  ['id','batch_id','item','exp_date','prod_date']
    success_url = reverse_lazy('invent:inventbatch')
    permission_required = "invent.add_inventbatch"
    title = model._meta.verbose_name


class InventBatchUpdateView(custom.ObjectUpdateView):
    model = InventBatch
    fields = ['batch_id','item','exp_date','prod_date']
    success_url = reverse_lazy('invent:inventbatch')
    permission_required = "invent.change_inventbatch"
    title = model._meta.verbose_name


class InventBatchDeleteView(custom.ObjectDeleteView):
    model = InventBatch
    success_url = reverse_lazy('invent:inventbatch')
    permission_required = "invent.delete_inventbatch"
    title = model._meta.verbose_name