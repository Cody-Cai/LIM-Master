from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import JsonResponse, HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils import translation
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import messages
from .models.basic import VendGroup, VendTable, VendAddress, VendContact
from .forms import VendAddressForm, VendContactForm
from utils import custom

import json


class VendGroupListView(PermissionRequiredMixin, generic.ListView):
    model = VendGroup
    template_name = "vend/vendgroup_list.html"
    permission_required = "vend.view_vendgroup"


class VendGroup_Json(custom.JSONResponseMixin):
    permission_required = "vend.view_vendgroup"

    def get_data(self, context):
        fields = ['id','code','name']
        ret = dict(data=list(VendGroup.objects.values(*fields)))
        return super().get_data(ret)


class VendGroupCreateView(custom.ObjectCreateView):
    model = VendGroup
    fields = '__all__'
    success_url = reverse_lazy('vend:vendgroup')
    permission_required = "vend.add_vendgroup"
    title = model._meta.verbose_name


class VendGroupUpdateView(custom.ObjectUpdateView):
    model = VendGroup
    fields = ['code','name']
    success_url = reverse_lazy('vend:vendgroup')
    permission_required = "vend.change_vendgroup"
    title = model._meta.verbose_name


class VendGroupDeleteView(custom.ObjectDeleteView):
    model = VendGroup
    title = model._meta.verbose_name
    success_url = reverse_lazy('vend:vendgroup')
    permission_required = "vend.delete_vendgroup"


class VendTableListView(PermissionRequiredMixin, generic.ListView):
    model = VendTable
    template_name = "vend/vendtable_list.html"
    permission_required = "vend.view_vendtable"


class VendTable_Json(custom.JSONResponseMixin):
    permission_required = "vend.view_vendtable"

    def get_data(self, context):
        fields = ['id','account_num','name','short_name','vend_group__code','invoice_account__account_num','currency__code']
        ret = dict(data=list(VendTable.objects.values(*fields)))
        return super().get_data(ret)


class VendTableCreateView(custom.ObjectCreateView):
    model = VendTable
    fields = ['id','account_num','name','short_name','vend_group','currency']
    success_url = reverse_lazy('vend:vendtable')
    permission_required = "vend.add_vendtable"
    title = model._meta.verbose_name

    def form_valid(self, form): 
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class VendTableUpdateView(custom.ObjectUpdateView):
    model = VendTable
    fields = ['id','account_num','name','short_name','vend_group','invoice_account','currency','countryregion','url','main_contact','language','dlv_term',
            'dlv_mode','dlv_destination','paym_term','tax_group','incl_tax','notes','blocked']
    template_name = "vend/vendtable_update.html"
    success_url = reverse_lazy('vend:vendtable')
    permission_required = "vend.change_vendtable"
    title = model._meta.verbose_name

    def form_valid(self, form): 
        if form.has_changed():
            form.instance.modified_by = self.request.user
        return super().form_valid(form)


class VendTableDeleteView(custom.ObjectDeleteView):
    model = VendTable
    success_url = reverse_lazy('vend:vendtable')
    permission_required = "vend.delete_vendtable"
    title = model._meta.verbose_name


# Not use
@permission_required("vend.add_vendaddress", raise_exception=True)
def create_vendaddress(request, pk):
    vendtable = VendTable.objects.get(id=pk)
    vendaddresses = VendAddress.objects.filter(vendtable=vendtable)
    form = VendAddressForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            vendaddresses = form.save(commit=False)
            vendaddresses.vendtable = vendtable
            vendaddresses.save()
            return redirect("vend:vendaddress-detail", pk=vendaddresses.id)
            
    context = {
        "form": form,
        "objtable": vendtable
    }

    return render(request, "vend/vendaddress_form.html", context)


class VendAddressCreateView(custom.ObjectCreateView):
    model = VendAddress
    form_class = VendAddressForm
    permission_required = 'vend.add_vendaddress'
    template_name = "vend/vendaddress_form.html"
    title = model._meta.verbose_name

    def get(self, request, *args, **kwargs):
        vendtable = get_object_or_404(VendTable, pk=kwargs["vendtable_id"])
        self.initial = {"vendtable": vendtable}
        return super().get(request, *args, **kwargs)

        
# Not use
@permission_required("vend.change_vendaddress", raise_exception=True)
def update_vendaddress(request, pk):
    vendaddress = get_object_or_404(VendAddress, id=pk)
    form = VendAddressForm(request.POST or None, instance=vendaddress)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("vend:vendaddress-detail", pk=vendaddress.id)

    context = {
        "form": form,
        "vendaddress": vendaddress
    }

    return render(request, "vend/vendaddress_form.html", context)


class VendAddressUpdateView(custom.ObjectUpdateView):
    model = VendAddress
    form_class = VendAddressForm
    #fields = ["name",'is_primary',"addresstype","address",'zipcode','city','State','countryregion']
    permission_required = 'vend.change_vendaddress'
    template_name = "vend/vendaddress_form.html"
    title = model._meta.verbose_name


class VendAddressDetailView(PermissionRequiredMixin, generic.DetailView):
    model = VendAddress
    permission_required = 'vend.view_vendaddress'
    template_name = "vend/vendaddress_detail.html"


class VendAddressDeleteView(custom.ObjectDeleteView):
    model = VendAddress
    success_url = reverse_lazy('vend:vendtable')
    permission_required = "vend.delete_vendaddress"
    title = model._meta.verbose_name


class VendContactCreateView(custom.ObjectCreateView):
    model = VendContact
    form_class = VendContactForm
    permission_required = 'vend.add_vendcontact'
    template_name = "vend/vendcontact_form.html"
    title = model._meta.verbose_name

    def get(self, request, *args, **kwargs):
        vendtable = get_object_or_404(VendTable, pk=kwargs["vendtable_id"])
        self.initial = {"vendtable": vendtable}
        return super().get(request, *args, **kwargs)


class VendContactUpdateView(custom.ObjectUpdateView):
    model = VendContact
    form_class = VendContactForm
    #fields = ["name",'is_primary',"addresstype","address",'zipcode','city','State','countryregion']
    permission_required = 'vend.change_vendcontact'
    template_name = "vend/vendcontact_form.html"
    title = model._meta.verbose_name


class VendContactDetailView(PermissionRequiredMixin, generic.DetailView):
    model = VendContact
    permission_required = 'vend.view_vendcontact'
    template_name = "vend/vendcontact_detail.html"
    title = model._meta.verbose_name


class VendContactDeleteView(custom.ObjectDeleteView):
    model = VendContact
    success_url = reverse_lazy('vend:vendtable')
    permission_required = "vend.delete_vendcontact"
    title = model._meta.verbose_name