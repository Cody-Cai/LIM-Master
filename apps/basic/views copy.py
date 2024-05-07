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
from .models import CountryRegion, Currency, CompanyInfo, CompanyAddress, Unit, UnitTxt
from .forms import CompanyForm, CompanyAddressForm

import json

# Create your views here.
class CountryListView(PermissionRequiredMixin, generic.ListView):
    model = CountryRegion
    context_object_name = "country_list"
    template_name = "basic/country_list.html"
    permission_required = "basic.view_countryregion"


class CountryList_Json(PermissionRequiredMixin, View):
    permission_required = "basic.view_countryregion"

    def get(self, reqeust):
        #data = CountryRegion.objects.all()
        fields = ['id','code','name','en_name']
        ret = dict(data=list(CountryRegion.objects.values(*fields)))
        return JsonResponse(ret)


class CountryCreateView(PermissionRequiredMixin, CreateView):
    model = CountryRegion
    fields = '__all__'
    template_name = "basic/country_form.html"
    success_url = reverse_lazy('basic:country')
    permission_required = "basic.add_countryregion"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Country/Region %(name)s created") % {"name": form.instance.code}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class CountryUpdateView(PermissionRequiredMixin, UpdateView):
    model = CountryRegion
    fields = '__all__'
    template_name = "basic/country_form.html"
    success_url = reverse_lazy('basic:country')
    permission_required = "basic.change_countryregion"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Country/Region %(name)s updated") % {"name": form.instance.code}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class CountryDeleteView(PermissionRequiredMixin, DeleteView):
    model = CountryRegion
    template_name = "basic/country_delete.html"
    success_url = reverse_lazy('basic:country')
    permission_required = "basic.delete_countryregion"
    
    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Country/Region %(name)s deleted") % {"name": self.object}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class CurrencyListView(PermissionRequiredMixin, generic.ListView):
    model = Currency
    context_object_name = "currency_list"
    template_name = "basic/currency_list.html"
    permission_required = "basic.view_currency"


class CurrencyList_Json(PermissionRequiredMixin, View):
    permission_required = "basic.view_currency"

    def get(self, reqeust):
        fields = ['id','code','name','symbol']
        ret = dict(data=list(Currency.objects.values(*fields)))
        return JsonResponse(ret)


class CurrencyCreateView(PermissionRequiredMixin, CreateView):
    model = Currency
    fields = '__all__'
    template_name = "basic/currency_form.html"
    success_url = reverse_lazy('basic:currency')
    permission_required = "basic.add_currency"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Currency %(name)s created") % {"name": form.instance.code}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class CurrencyUpdateView(PermissionRequiredMixin, UpdateView):
    model = Currency
    fields = '__all__'
    template_name = "basic/currency_form.html"
    success_url = reverse_lazy('basic:currency')
    permission_required = "basic.change_currency"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Currency %(name)s updated") % {"name": form.instance.code}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class CurrencyDeleteView(PermissionRequiredMixin, DeleteView):
    model = Currency
    template_name = "basic/currency_delete.html"
    success_url = reverse_lazy('basic:currency')
    permission_required = "basic.delete_currency"
    
    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Currency %(name)s deleted") % {"name": self.object}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class CompanyInfoView(PermissionRequiredMixin,View):
    form_class = CompanyForm
    company = get_object_or_404(CompanyInfo, pk=1)
    initial = company
    template_name = "basic/company_form.html"
    permission_required = ["basic.view_companyinfo"]

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.initial)
        return render(request, self.template_name, {"form": form, "companyinfo": self.company})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,instance=self.initial)
        if form.is_valid():
            # <process form cleaned data>
            form.save()
            messages.success(request, _('Company Info was updated successfully!'))
            return redirect(to="basic:company")

        return render(request, self.template_name, {"form": form})

@login_required
@permission_required("basic.add_companyaddress", raise_exception=True)
def create_companyaddress(request, pk):
    company = CompanyInfo.objects.get(id=pk)
    companyaddresses = CompanyAddress.objects.filter(company=company)
    form = CompanyAddressForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            companyaddress = form.save(commit=False)
            companyaddress.company = company
            companyaddress.save()
            return redirect("basic:companyaddress-detail", pk=companyaddress.id)
        else:
            return render(request, "basic/companyaddress_form.html", context={
                "addform": form
            })

    context = {
        "addform": form,
        "company": company
    }

    return render(request, "basic/companyaddress_form.html", context)


@permission_required("basic.change_companyaddress", raise_exception=True)
def update_companyaddress(request, pk):
    companyaddress = get_object_or_404(CompanyAddress, id=pk)
    form = CompanyAddressForm(request.POST or None, instance=companyaddress)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("basic:companyaddress-detail", pk=companyaddress.id)

    context = {
        "addform": form,
        "companyaddress": companyaddress
    }

    return render(request, "basic/companyaddress_form.html", context)


@permission_required("basic.view_companyaddress", raise_exception=True)
def detail_companyaddress(request, pk):
    companyaddress = get_object_or_404(CompanyAddress, id=pk)
    context = {
        "comAdd": companyaddress
    }
    return render(request, "basic/companyaddress_detail.html", context)


@permission_required("basic.delete_companyaddress", raise_exception=True)
def delete_companyaddress(request, pk):
    companyaddress = get_object_or_404(CompanyAddress, id=pk)
    companyaddress.delete()
    # return HttpResponse("")

    return HttpResponse(
        "",
        headers={
            'HX-Trigger': json.dumps({
                "showMessage": f"{companyaddress.name} deleted."
            })
        })


class UnitListView(PermissionRequiredMixin, generic.ListView):
    model = Unit
    template_name = "basic/unit_list.html"
    permission_required = "basic.view_unit"


class Unit_Json(PermissionRequiredMixin, View):
    permission_required = "basic.view_unit"

    def get(self, reqeust):
        unit = Unit.objects.all()
        fields = ['id','unit_id', 'txt','unit_decimals','symbol']
        ret = dict(data=list(Unit.objects.values(*fields)))
        return JsonResponse(ret)


class UnitCreateView(PermissionRequiredMixin, CreateView):
    model = Unit
    fields = '__all__'
    template_name = "common/offcanvas_form.html"
    success_url = reverse_lazy('basic:unit')
    permission_required = "basic.add_unit"
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


class UnitUpdateView(PermissionRequiredMixin, UpdateView):
    model = Unit
    fields = ['id','unit_id', 'txt','unit_decimals','symbol']
    template_name = "common/offcanvas_form.html"
    success_url = reverse_lazy('basic:unit')
    permission_required = "basic.change_unit"
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


class UnitDeleteView(PermissionRequiredMixin, DeleteView):
    model = Unit
    template_name = "common/modal_delete.html"
    success_url = reverse_lazy('basic:unit')
    permission_required = "basic.delete_unit"
    title = model._meta.verbose_name

    def form_valid(self, form):
        try:
            super().form_valid(form)
            msg = _("%(title)s %(name)s deleted") % {"title": self.title, "name": self.object}
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