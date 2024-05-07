from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from .forms import LoginForm, SignUpForm, UserCreateForm, UpdateUserForm, UpdateProfileForm, UserForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group, Permission
from django.views import generic, View
from django.http import JsonResponse, HttpResponse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import User, Profile
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.text import format_lazy
from django.contrib.gis.geoip2 import GeoIP2
from datetime import datetime

import json

# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm
    redirect_authenticated_user=True                        
    template_name = "accounts/login.html"
    authentication_form=LoginForm

    def form_valid(self, form):
        g = GeoIP2()
        remember_me = form.cleaned_data.get('remember_me')
        username = form.cleaned_data.get('username')
        self.request.session['user_name'] = username
        login_datetime = datetime.now()
        #print(login_datetime)
        self.request.session['login_dt'] = login_datetime.strftime('%Y-%m-%d %H:%M:%S')
        ip_add = self.request.META.get("REMOTE_ADDR")
        #ip_add = "205.186.163.125"
        self.request.session['ip_add'] = ip_add
        try:
            res = g.city(ip_add)
            self.request.session['city'] = res['city']
            self.request.session['country'] = "(%s) %s" % (res['country_code'],res['country_name'])
        except:
            self.request.session['city'] = "None"
            self.request.session['country'] = "None"

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('login')


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = User
    template_name = "accounts/user_list.html"
    permission_required = "authentication.view_user"
    

class UserList_Json(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "authentication.view_user"
    def get(self, request):
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser']
        data = dict(data=list(User.objects.values(*fields).order_by('-date_joined')))
        #response = {'data': ret}
        return JsonResponse(data)


class UserCreateView(PermissionRequiredMixin, View):
    form_class = UserCreateForm
    permission_required = "authentication.add_user"
    initial = {'key': 'value'}
    template_name = 'accounts/user_create.html'
    form_name = _('Add User')
    error_class = "list-unstyled"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form, "form_name": self.form_name})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            msg = _("User %(name)s created") % {"name": username}
            #messages.success(request, f'Account created for {username}')
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "reloadTable": None,
                        "showMessage": f'{msg}'
                    })
                })

        return render(request, self.template_name, {'form': form, 'form_name': self.form_name})


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    permission_required = "authentication.change_user"
    form_class = UserForm
    template_name = 'accounts/user_update.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("User %(name)s updated") % {"name": form.instance.username}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class UserDeleteView(PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = "authentication.delete_user"
    template_name = "accounts/user_delete.html"
    success_url = reverse_lazy('users')
    
    def form_valid(self, form):
        super().form_valid(form)
        msg = _("User %(name)s deleted") % {"name": self.object}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class ChangePasswordView(SuccessMessageMixin, PermissionRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_message = _("Successfully Changed Your Password!")
    success_url = reverse_lazy('profile')
    permission_required = "authentication.change_password"

    def form_valid(self, form):       
        super().form_valid(form)
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadpage": None
                })
            })
        

class SetPasswordView(PermissionRequiredMixin, View):
    form_class = SetPasswordForm
    template_name = 'accounts/password_reset.html'
    form_name = _("Password Reset")
    permission_required = "authentication.set_password"
    
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        form = SetPasswordForm(user)
        return render(request, self.template_name, {"form": form, "form_name": self.form_name})

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        form = self.form_class(user,request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            username = user.get_username()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "showMessage": f'{username}''s Password has been set. '
                    })
                })

        return render(request, self.template_name, {'form': form, 'form_name': self.form_name})

@login_required
@permission_required("authentication.view_profile", raise_exception=True)
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile = get_object_or_404(Profile, user=request.user)
        # get the init value
        employee_post = profile.employee 
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        #print(request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            profile_form.instance.employee = employee_post  # keep the init value
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile is updated successfully'))
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'accounts/profile.html', {'user_form': user_form, 'profile_form': profile_form})


class SetUserProfileView(PermissionRequiredMixin, View):
    template_name = 'accounts/user_profile.html'
    permission_required = "authentication.set_profile"

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        profile = get_object_or_404(Profile, user=user)
        form = UpdateProfileForm(instance=profile)
        return render(request, self.template_name, {"form": form, "user": user})

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        profile = get_object_or_404(Profile, user=user)
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            username = user.get_username()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "showMessage": f'{username}''s Profile updated. '
                    })
                })

        return render(request, self.template_name, {'form': form, "user": user})


class UserPermissionsView(PermissionRequiredMixin, UpdateView):
    model = User
    fields = ['username','groups','user_permissions']
    template_name = "accounts/user_permissions.html"
    success_url = reverse_lazy('users')
    permission_required = "auth.view_permission"

    def form_valid(self, form):       
        response = super().form_valid(form)
        messages.success(self.request, _('The user %(name)s was changed successfully.') % {"name": form.instance.username})
        return response


class GroupList_Json(PermissionRequiredMixin, View):
    permission_required = "auth.view_group"

    def get(self, reqeust):
        fields = ['id','name','description']
        ret = dict(data=list(Group.objects.values(*fields)))
        return JsonResponse(ret)


class GroupListView(PermissionRequiredMixin, generic.ListView):
    model = Group
    template_name = "accounts/group_list.html"
    permission_required = "auth.view_group"


class GroupCreateView(PermissionRequiredMixin, CreateView):
    model = Group
    fields = '__all__'
    template_name = "accounts/group_form.html"
    success_url = reverse_lazy('group-create')
    permission_required = "auth.add_group"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Group %(name)s created") % {"name": form.instance.name}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })

        
class GroupUpdateView(PermissionRequiredMixin, UpdateView):
    model = Group
    fields = ['name','description']
    template_name = "accounts/group_form.html"
    success_url = reverse_lazy('group')
    permission_required = "auth.change_group"

    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Group %(name)s updated") % {"name": form.instance.name}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


class GroupDeleteView(PermissionRequiredMixin, DeleteView):
    model = Group
    template_name = "accounts/group_delete.html"
    success_url = reverse_lazy('group')
    permission_required = "auth.delete_group"
    
    def form_valid(self, form):
        super().form_valid(form)
        msg = _("Group %(name)s deleted") % {"name": self.object}
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reloadTable": None,
                    "showMessage": f'{msg}'
                })
            })


def testView(request):
    User = get_user_model()
    fullname = User.get_full_name(request.user)
    #return render(request, 'accounts/test2.html', {'fullname': fullname} )
    return render(request, 'system/testDatatable.html')


class GroupPermissionsView(PermissionRequiredMixin, UpdateView):
    model = Group
    fields = ['name','permissions']
    template_name = "accounts/group_permissions.html"
    success_url = reverse_lazy('group')
    permission_required = "authentication.view_permission"

    def form_valid(self, form):       
        response = super().form_valid(form)
        messages.success(self.request, _('The group %(name)s was changed successfully.') % {"name": form.instance.name})
        return response
        
