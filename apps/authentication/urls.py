from django.urls import path
from .views import login_view, register_user, logout_view, ChangePasswordView, profile
from django.contrib.auth.views import LogoutView

app_name = "auth"
urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile, name="profile"),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]