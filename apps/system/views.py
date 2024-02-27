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
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.utils import timezone

# Create your views here.
import datetime
import json
import zoneinfo

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
        #sessions = Session.objects.iterator() # also works with Session.objects.get_queryset()
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in sessions: # iterate over sessions
            data = session.get_decoded() # decode the session data
            data["session_key"] = session.session_key
            data["expire_date"] = session.expire_date # normally the data doesn't include the session key, so add it
            #print(data)

        #print(request.session.get("django_timezone"))
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

    def get_context_data(self, **kwargs):
        # for key, value in self.request.session.items():
        #     print('{} => {}'.format(key, value))

        # Call the base implementation first to get the context
        context = super(LanguageListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        #context['some_data'] = self.request.session.get('_auth_user_backend','default')
        context['some_data'] = self.request.META.get("REMOTE_ADDR")
        return context


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
        # s = SessionStore(session_key="ipzwklmuvacwufbgyrojfml0k5elve1e")
        # s.delete()
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
        #print(Menu.objects.values(*fields))
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
    

class SessionListView(PermissionRequiredMixin, generic.ListView):
    model = Session
    template_name = "system/session_list.html"
    permission_required = "sessions.view_session"


class SessionList_Json(PermissionRequiredMixin, View):
    permission_required = "sessions.view_session"

    def get(self, reqeust): 
        local_tz = zoneinfo.ZoneInfo('Asia/Shanghai')
        session_json = []
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        #print(sessions)
        for session in sessions: # iterate over sessions
            session_data = session.get_decoded() # decode the session data
            #print(session_data)
            session_data["session_key"] = session.session_key # normally the data doesn't include the session key, so add it
            expiredate = session.expire_date
            session_data["expire_date"] = expiredate.astimezone(local_tz)
            if 'user_name' not in session_data:
                session_data["user_name"] = 'None'
            if 'login_dt' not in session_data:
                session_data["login_dt"] = 'None'
            if 'ip_add' not in session_data:
                session_data["ip_add"] = 'None'
            if 'city' not in session_data:
                session_data["city"] = 'None'
            if 'country' not in session_data:
                session_data["country"] = 'None'
            session_data["select"] = 'selection'
            session_json.append(session_data)
        
        #print(session_json)
        response = {'data': session_json}
        return JsonResponse(response)


class SessionDeleteView(PermissionRequiredMixin, DeleteView):
    model = Session
    template_name = "system/session_delete.html"
    success_url = reverse_lazy('system:session')
    permission_required = "sessions.delete_session"
    
    def form_valid(self, form):
        # s = SessionStore(session_key="ipzwklmuvacwufbgyrojfml0k5elve1e")
        # s.delete()
        #print(self.object.pk)
        msg = _("Session %(name)s deleted") % {"name": self.object.pk}
        super().form_valid(form)
        #msg = 'Session Deleted!'
        #msg = _("Session %(name)s deleted") % {"name": self.object}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })

# not use
def delete_session(request):
    if request.method == "POST":
        idlist = request.POST.getlist("selection")
        #print(request)
        #print(idlist)
        Session.objects.filter(session_key__in=id_list).delete()
        return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "reloadTable": None,
                "showMessage": f"{id_list} deleted."
            })
        })
    else:
        idlist = request.GET.getlist("selection")
        #print(idlist)

    return render(request, 'system/session_delete_confirm.html', {
        'ids': idlist,
    })


class delete_SessionView(PermissionRequiredMixin, View):
    template_name = 'system/session_delete_confirm.html'
    permission_required = "sessions.delete_session"

    def get(self, request, *args, **kwargs):
        idlist = list(map(str,kwargs["pks"].split(',')))
        #print(request.GET.getList(['selection']))
        # selected_products = request.GET.getlist("selection")
        # print(selected_products)
        #print(idlist)
        return render(request, self.template_name, {'ids': idlist})

    def post(self, request, *args, **kwargs):
        idlist = list(map(str,kwargs["pks"].split(',')))
        session = Session.objects.filter(session_key__in=idlist).delete()
        #print(session)
        return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "reloadTable": None,
                "showMessage": f"{idlist} deleted."
            })
        })

        #return render(request, self.template_name, {'ids': idlist})