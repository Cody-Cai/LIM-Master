from django.contrib.auth.forms import UserCreationForm, UserCreationForm, AuthenticationForm
from django import forms
from django.forms import ModelForm, TextInput, HiddenInput, FileInput, Select
from .models import User, Profile
from django.utils.translation import gettext_lazy as _

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    firstname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        ))
    lastname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UpdateUserForm(ModelForm):
    class Meta:
        model =  User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            "username": HiddenInput(),
            "email": TextInput(attrs={'class': 'form-control'}),
            "first_name": TextInput(attrs={'class': 'form-control'}),
            "last_name": TextInput(attrs={'class': 'form-control'}),
        }

class UpdateProfileForm(ModelForm):
    #avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control','type':"file"}))

    class Meta:
        model = Profile
        fields = ['avatar','employee']
        widgets = {
            "avatar": FileInput(attrs={'class': 'form-control','type':"file"}),
            "employee": Select(attrs={'class': 'form-control'}),
        }


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2','is_superuser','is_active']


class UserForm(ModelForm):
    class Meta:
        model =  User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_active']