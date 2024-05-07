from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext, gettext_lazy as _
from django.db import models

import json


class JSONResponseMixin(PermissionRequiredMixin, View):
    """
    A mixin that can be used to render a JSON response.
    """
    context = None

    def render_to_json_response(self, context):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(self.get_data(context))

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context

    def get(self, reqeust):
        return self.render_to_json_response(self.context)


class ObjectCreateView(PermissionRequiredMixin, CreateView):
    """
    A mixin that can be used to render a create view for modal or offcanvas.
    """
    template_name = "common/offcanvas_form.html"

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


class ObjectUpdateView(PermissionRequiredMixin, UpdateView):
    """
    A mixin that can be used to render a create view for modal or offcanvas.
    """
    template_name = "common/offcanvas_form.html"

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


class ObjectDeleteView(PermissionRequiredMixin, DeleteView):
    """
    A mixin that can be used to render a create view for modal or offcanvas.
    """
    title = None
    template_name = "common/modal_delete.html"

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