from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import messages
from django.db import IntegrityError
from .models import OrganizationUnit, PersonTitle, Employee
from .forms import EmployeeForm


import json


class OrganizationUnitView(PermissionRequiredMixin, generic.ListView):
    model = OrganizationUnit
    context_object_name = "organizationunit_list"
    template_name = "hrm/organizationunit_list.html"
    permission_required = "hrm.view_organizationunit"


class OrganizationUnit_Json(PermissionRequiredMixin, View):
    permission_required = "hrm.view_organizationunit"

    def get(self, reqeust):
        organizationunit = OrganizationUnit.objects.all()
        fields = ['id', 'unitid', 'description', 'parentunit', 'parentunit__unitid']
        ret = dict(data=list(OrganizationUnit.objects.values(*fields)))
        return JsonResponse(ret)


class OrganizationUnitCreateView(PermissionRequiredMixin, CreateView):
    model = OrganizationUnit
    fields = '__all__'
    template_name = "hrm/organizationunit_form.html"
    success_url = reverse_lazy('hrm:organization')
    permission_required = "hrm.add_organizationunit"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("%(title)s %(name)s created") % {"title": _("Organization unit"), "name": form.instance.unitid}
        #print(msg)
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class OrganizationUnitUpdateView(PermissionRequiredMixin, UpdateView):
    model = OrganizationUnit
    fields = ['id', 'unitid', 'description', 'parentunit']
    template_name = "hrm/organizationunit_form.html"
    success_url = reverse_lazy('hrm:organization')
    permission_required = "hrm.change_organizationunit"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("%(title)s %(name)s updated") % {"title": _("Organization unit"), "name": form.instance.unitid}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class OrganizationUnitDeleteView(PermissionRequiredMixin, DeleteView):
    model = OrganizationUnit
    template_name = "hrm/organizationunit_delete.html"
    success_url = reverse_lazy('hrm:organization')
    permission_required = "hrm.delete_organizationunit"
    
    def form_valid(self, form):
        super().form_valid(form)
        msg = _("%(title)s %(name)s deleted") % {"title": _("Organization unit"), "name": form.instance.unitid}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class PersonTitleView(PermissionRequiredMixin, generic.ListView):
    model = PersonTitle
    #context_object_name = "persontitle_list"
    template_name = "hrm/persontitle_list.html"
    permission_required = "hrm.view_persontitle"


class PersonTitle_Json(PermissionRequiredMixin, View):
    permission_required = "hrm.view_persontitle"

    def get(self, reqeust):
        persontitle = PersonTitle.objects.all()
        fields = ['id', 'name']
        ret = dict(data=list(PersonTitle.objects.values(*fields)))
        return JsonResponse(ret)


class PersonTitleCreateView(PermissionRequiredMixin, CreateView):
    model = PersonTitle
    fields = '__all__'
    template_name = "common/offcanvas_form.html"
    success_url = reverse_lazy('hrm:persontitle')
    permission_required = "hrm.add_persontitle"
    title = model._meta.verbose_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("%(title)s %(name)s created") % {"title": self.title, "name": self.object}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class PersonTitleUpdateView(PermissionRequiredMixin, UpdateView):
    model = PersonTitle
    fields = ['id', 'name']
    template_name = "common/offcanvas_form.html"
    success_url = reverse_lazy('hrm:persontitle')
    permission_required = "hrm.change_persontitle"
    title = model._meta.verbose_name

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("%(title)s %(name)s updated") % {"title": self.title, "name": self.object}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class PersonTitleDeleteView(PermissionRequiredMixin, DeleteView):
    model = PersonTitle
    template_name = "common/modal_delete.html"
    success_url = reverse_lazy('hrm:persontitle')
    permission_required = "hrm.delete_persontitle"
    
    def form_valid(self, form):
        try:
            super().form_valid(form)
            msg = _("%(title)s %(name)s deleted") % {"title": _("Person title"), "name": self.object}
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "reloadTable": None,
                        "showMessage": f'{msg}'
                    })
                })
        except IntegrityError as e:
            #messages.error(self.request, str(e))
            self.object = self.get_object()
            context = self.get_context_data(object=self.object, error=str(e))
            return self.render_to_response(context)


class EmployeeView(PermissionRequiredMixin, generic.ListView):
    model = Employee
    #context_object_name = "persontitle_list"
    template_name = "hrm/employee_list.html"
    permission_required = "hrm.view_employee"


class Employee_Json(PermissionRequiredMixin, View):
    permission_required = "hrm.view_employee"

    def get(self, reqeust):
        employees= Employee.objects.all()
        #fields = ['id','emplid','name','title__name','orgnization_unit__unitid','status']
        #ret = dict(data=list(Employee.objects.values(*fields)))
        data = [emp.get_data() for emp in employees]
        ret = {'data': data}
        #print(data)
        return JsonResponse(ret)


class EmployeeCreateView(PermissionRequiredMixin, CreateView):
    model = Employee
    fields = ['id','emplid','name','title','orgnization_unit','status']
    template_name = "hrm/employee_form.html"
    success_url = reverse_lazy('hrm:employee')
    permission_required = "hrm.add_employee"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        super().form_valid(form)
        msg = _("%(title)s %(name)s created") % {"title": _("Employee"), "name": self.object}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class EmployeeUpdateView(PermissionRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    #fields = '__all__' #['id','emplid','name','title','orgnization_unit','status','employee_type','marital_status','gender']
    template_name = "hrm/employee_update.html"
    success_url = reverse_lazy('hrm:employee')
    permission_required = "hrm.change_employee"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("%(title)s %(name)s updated") % {"title": _("Employee"), "name": self.object}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class EmployeeDetailsView(PermissionRequiredMixin, UpdateView):
    model = Employee
    fields = "__all__"
    template_name = "hrm/employee_update.html"
    success_url = reverse_lazy('hrm:employee')
    permission_required = "hrm.change_employee"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("%(title)s %(name)s updated") % {"title": _("Employee"), "name": self.object}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class EmployeeDeleteView(PermissionRequiredMixin, DeleteView):
    model = Employee
    template_name = "hrm/employee_delete.html"
    success_url = reverse_lazy('hrm:employee')
    permission_required = "hrm.delete_employee"
    
    def form_valid(self, form):
        super().form_valid(form)
        msg = _("%(title)s %(name)s deleted") % {"title": _("Employee"), "name": self.object}
        
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })
