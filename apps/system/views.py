from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy, resolve
from django.utils.translation import gettext, gettext_lazy as _
from .models import Language, Menu, MenuLangName
from django.utils.translation import get_language_info
from django.core.exceptions import ValidationError
from django.core import serializers
from django.contrib.auth.models import Permission

# Create your views here.
import datetime
import json

User = get_user_model()

#Handle error page
def error_404_view(request, exception):  
    return render(request, 'system/errors/404.html')


def error_500_view(request):  
    return render(request, 'system/errors/500.html')


def error_403_view(request, exception):  
    return render(request, 'system/errors/403.html')


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        # match  = resolve(request.path_info)
        # print(request.path_info)
        # print(match.url_name)
        # print(match.app_name)
        # print(match.view_name)
        menu_nav = Menu.objects.filter(menutype="N")
        menu_top = menu_nav.get(url="system:system")
        menu_side = Menu.objects.filter(parent = menu_top)
        menu_home = menu_side.filter(is_home=True)[0]

        context = {
            'menu_nav': menu_nav,
            'menu_side': menu_side,
            'menu_home': menu_home,
        }
        return render(request, 'home/ihome.html', context=context)


class starterView(LoginRequiredMixin, View):
    def get(self, request):
        #print(request.path_info)
        #print(reverse('system:starter'))
        match  = resolve(request.path_info)
        # print(match.url_name)
        # print(match.app_name)
        # print(match.view_name)
        menu_nav = Menu.objects.filter(menutype="N")
        menu_home = menu_nav.get(name="System")
        menu_side = Menu.objects.filter(parent = menu_home)

        context = {
            'menu_nav': menu_nav,
            'menu_side': menu_side,
            'menu_home': menu_home,
        }
        return render(request, 'system/starter.html', context=context)


class LanguageListView(PermissionRequiredMixin, generic.ListView):
    model = Language
    template_name = "system/language_list.html"
    permission_required = "system.view_language"


class Language_Json(PermissionRequiredMixin, View):
    permission_required = "system.view_language"

    def get(self, reqeust, *args, **kwargs):
        code=str(reqeust.GET['code'])
        data = {}
        error_msg = {}
        if code:
            try:
                data = get_language_info(code)
            except KeyError as ke:
                error_msg = {'errmsg': f'{ke}'}

        #print(error_msg)
        Langs = {'data':data,'msg':error_msg}
        return JsonResponse(Langs)


class LanguageList_Json(PermissionRequiredMixin, View):
    permission_required = "system.view_language"

    def get(self, reqeust):
        Langs = Language.objects.all()
        data = [lang.get_data() for lang in Langs]
        response = {'data': data}
        return JsonResponse(response)


class LanguageCreateView(PermissionRequiredMixin, CreateView):
    model = Language
    fields = '__all__'
    template_name = "system/language_form.html"
    success_url = reverse_lazy('system:language')
    permission_required = "system.add_language"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Language %(name)s created") % {"name": form.instance.code}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class LanguageUpdateView(PermissionRequiredMixin, UpdateView):
    model = Language
    fields = '__all__'
    template_name = "system/language_form.html"
    success_url = reverse_lazy('system:language')
    permission_required = "system.change_language"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Language %(name)s updated") % {"name": form.instance.code}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class LanguageDeleteView(PermissionRequiredMixin, DeleteView):
    model = Language
    template_name = "system/language_delete.html"
    success_url = reverse_lazy('system:language')
    permission_required = "system.delete_language"
    
    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Language %(name)s deleted") % {"name": self.object}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class MenuListView(PermissionRequiredMixin, generic.ListView):
    model = Menu
    context_object_name = "menu_list"
    template_name = "system/menu_list.html"
    permission_required = "system.view_menu"


class MenuList_Json(PermissionRequiredMixin, View):
    permission_required = "system.view_menu"

    def get(self, reqeust):
        menu = Menu.objects.all()
        fields = ['id', 'icon', 'is_home', 'menutype', 'name', 'parent', 'parent__name','permission__codename', 'seq', 'url']
        ret = dict(data=list(Menu.objects.values(*fields)))
        return JsonResponse(ret)


class MenuCreateView(PermissionRequiredMixin, CreateView):
    model = Menu
    fields = '__all__'
    template_name = "system/Menu_form.html"
    success_url = reverse_lazy('system:menu')
    permission_required = "system.add_menu"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        super().form_valid(form)
        msg = _("Menu item %(name)s created") % {"name": form.instance.name}
        #print(msg)
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class MenuUpdateView(PermissionRequiredMixin, UpdateView):
    model = Menu
    fields = ['icon', 'is_home', 'menutype', 'name', 'parent','permission', 'seq', 'url']
    template_name = "system/menu_form.html"
    success_url = reverse_lazy('system:menu')
    permission_required = "system.change_menu"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Menu %(name)s updated") % {"name": form.instance.name}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class MenuDeleteView(PermissionRequiredMixin, DeleteView):
    model = Menu
    template_name = "system/menu_delete.html"
    success_url = reverse_lazy('system:menu')
    permission_required = "system.delete_menu"
    
    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Menu %(name)s deleted") % {"name": self.object}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })



from .forms import MenuLangNameFormset
def manage_menulangname(request, pk):
    # author = get_object_or_404(Author, pk=pk)
    menu = Menu.objects.get(pk=pk)
    #BookInlineFormSet = inlineformset_factory(Author, Book, fields=('title','genre','language',),can_delete=True)
    if request.method == "POST":
        formset = MenuLangNameFormset(request.POST, request.FILES, instance=menu)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            #return HttpResponseRedirect(reverse_lazy('system:menu'))
            msg = _("Menu text of %(name)s updated") % {"name": menu.name}
            #print(msg)
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "reloadTable": None,
                        "showMessage": f'{msg}'
                    })
                })
    else:
        formset = MenuLangNameFormset(instance=menu)

    return render(request, 'system/manage_menutext.html', {
        'formset': formset, 
        'menu': menu,})

from django.forms import inlineformset_factory
# Just for test
def manage_books(request, pk):
    # author = get_object_or_404(Author, pk=pk)
    menu = Menu.objects.get(pk=pk)
    BookInlineFormSet = inlineformset_factory(Menu, MenuLangName, fields=("lang", "name"), extra=1, can_delete=True)
    if request.method == "POST":
        formset = BookInlineFormSet(request.POST, request.FILES, instance=menu)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(reverse_lazy('system:menu'))
    else:
        formset = BookInlineFormSet(instance=menu)

    return render(request, 'system/manage_menulangname_copy.html',{
        'formset': formset, 
        'menu': menu,})


class PermissionistView(PermissionRequiredMixin, generic.ListView):
    model = Permission
    context_object_name = "permission_list"
    template_name = "system/permission_list.html"
    permission_required = "auth.view_Permission"


class PermissionList_Json(PermissionRequiredMixin, View):
    permission_required = "auth.view_Permission"

    def get(self, reqeust): 
        fields = ['id','content_type__model','content_type__app_label','codename','name']
        ret = dict(data=list(Permission.objects.values(*fields)))
        return JsonResponse(ret)


class PermissionCreateView(PermissionRequiredMixin, CreateView):
    model = Permission
    fields = '__all__'
    template_name = "system/permission_form.html"
    success_url = reverse_lazy('system:permission')
    permission_required = "auth.add_Permission"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Permission %(name)s created") % {"name": form.instance.name}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class PermissionUpdateView(PermissionRequiredMixin, UpdateView):
    model = Permission
    fields = '__all__'
    template_name = "system/permission_form.html"
    success_url = reverse_lazy('system:permission')
    permission_required = "auth.change_Permission"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Permission %(name)s updated") % {"name": form.instance.name}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class PermissionDeleteView(PermissionRequiredMixin, DeleteView):
    model = Permission
    template_name = "system/permission_delete.html"
    success_url = reverse_lazy('system:permission')
    permission_required = "auth.delete_Permission"
    
    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Permission %(name)s deleted") % {"name": self.object}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })