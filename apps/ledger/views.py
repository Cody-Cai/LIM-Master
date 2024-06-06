from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import messages

from .models import TaxTable, TaxGroupHeading, TaxItemGroupHeading
from utils import custom

import json


class TaxTableListView(PermissionRequiredMixin, generic.ListView):
    model = TaxTable
    template_name = "ledger/taxtable_list.html"
    permission_required = "ledger.view_taxtable"


class TaxTable_Json(custom.JSONResponseMixin):
    permission_required = "ledger.view_taxtable"

    def get(self, request):
        taxtable = TaxTable.objects.all()
        data = [d.get_data() for d in taxtable]
        ret = {'data': data}
        return JsonResponse(ret)


class TaxTableCreateView(custom.ObjectCreateView):
    model = TaxTable
    fields = '__all__'
    success_url = reverse_lazy('ledger:taxtable')
    permission_required = "ledger.add_taxtable"
    title = model._meta.verbose_name


class TaxTableUpdateView(custom.ObjectUpdateView):
    model = TaxTable
    fields = '__all__'
    success_url = reverse_lazy('ledger:taxtable')
    permission_required = "ledger.change_taxtable"
    title = model._meta.verbose_name


class TaxTableDeleteView(custom.ObjectDeleteView):
    model = TaxTable
    success_url = reverse_lazy('ledger:taxtable')
    permission_required = "ledger.delete_taxtable"
    title = model._meta.verbose_name


class TaxGroupHeadingListView(PermissionRequiredMixin, generic.ListView):
    model = TaxGroupHeading
    template_name = "ledger/taxgroupheading_list.html"
    permission_required = "ledger.view_taxgroupheading"


class TaxGroupHeading_Json(custom.JSONResponseMixin):
    permission_required = "ledger.view_taxgroupheading"

    def get(self, request):
        taxgroup = TaxGroupHeading.objects.all()
        data = [d.get_data() for d in taxgroup]
        ret = {'data': data}
        return JsonResponse(ret)


class TaxGroupHeadingCreateView(custom.ObjectCreateView):
    model = TaxGroupHeading
    fields = '__all__'
    success_url = reverse_lazy('ledger:taxgroupheading')
    permission_required = "ledger.add_taxgroupheading"
    title = model._meta.verbose_name


class TaxGroupHeadingUpdateView(custom.ObjectUpdateView):
    model = TaxGroupHeading
    fields = '__all__'
    success_url = reverse_lazy('ledger:taxgroupheading')
    permission_required = "ledger.change_taxgroupheading"
    title = model._meta.verbose_name
    template_name = "common/offcanvas_form.html"


class TaxGroupHeadingDeleteView(custom.ObjectDeleteView):
    model = TaxGroupHeading
    success_url = reverse_lazy('ledger:taxgroupheading')
    permission_required = "ledger.delete_taxgroupheading"
    title = model._meta.verbose_name


class TaxItemGroupHeadingListView(PermissionRequiredMixin, generic.ListView):
    model = TaxItemGroupHeading
    template_name = "ledger/taxitemgroupheading_list.html"
    permission_required = "ledger.view_taxitemgroupheading"


class TaxItemGroupHeading_Json(custom.JSONResponseMixin):
    permission_required = "ledger.view_taxitemgroupheading"

    def get(self, request):
        taxitemgroup = TaxItemGroupHeading.objects.all()
        data = [d.get_data() for d in taxitemgroup]
        ret = {'data': data}
        return JsonResponse(ret)


class TaxItemGroupHeadingCreateView(custom.ObjectCreateView):
    model = TaxItemGroupHeading
    fields = '__all__'
    success_url = reverse_lazy('ledger:taxitemgroupheading')
    permission_required = "ledger.add_taxitemgroupheading"
    title = model._meta.verbose_name


class TaxItemGroupHeadingUpdateView(custom.ObjectUpdateView):
    model = TaxItemGroupHeading
    fields = '__all__'
    success_url = reverse_lazy('ledger:taxitemgroupheading')
    permission_required = "ledger.change_taxitemgroupheading"
    title = model._meta.verbose_name
    template_name = "common/offcanvas_form.html"


class TaxItemGroupHeadingDeleteView(custom.ObjectDeleteView):
    model = TaxItemGroupHeading
    success_url = reverse_lazy('ledger:taxitemgroupheading')
    permission_required = "ledger.delete_taxitemgroupheading"
    title = model._meta.verbose_name