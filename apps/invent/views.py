from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.views.generic.base import View, TemplateView
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import messages
from .models import ItemGroup, ItemColor, ItemConfig, ItemSize
from utils import custom

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