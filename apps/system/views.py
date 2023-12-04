from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.utils.translation import gettext, gettext_lazy as _
from .models import Language
from django.utils.translation import get_language_info
from django.core.exceptions import ValidationError

# Create your views here.
import json

User = get_user_model()

#Handle error page
def error_404_view(request, exception):  
    return render(request, 'system/errors/404.html')


def error_500_view(request):  
    return render(request, 'system/errors/500.html')


def error_403_view(request, exception):  
    return render(request, 'system/errors/403.html')

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
        print(msg)
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