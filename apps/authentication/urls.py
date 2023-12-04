from django.urls import path
from . import views
# login_view, register_user, logout_view, ChangePasswordView, profile, UserListView, UserList_Json, UserCreateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("test/", views.testView, name="test"),
    path('password-change/', views.ChangePasswordView.as_view(), name='password_change'),
    path('users/', views.UserListView.as_view(), name="users"),
    path('userJson/', views.UserList_Json.as_view(), name="user-Json"),
    path('user/create/', views.UserCreateView.as_view(), name="user-create"),
    path('user/<int:pk>/update/', views.UserUpdateView.as_view(), name="user-update"),
    path('user/<int:pk>/delete/', views.UserDeleteView.as_view(), name="user-delete"),
    path('user/<int:pk>/password_set/', views.SetPasswordView.as_view(), name="password_reset"),
    path('user/<int:pk>/update_profile/', views.SetUserProfileView.as_view(), name="user-profile"),
    path('user/<int:pk>/permissions/', views.UserPermissionsView.as_view(), name="user-permissions"),
    path('group/', views.GroupListView.as_view(), name="group"),
    path('groupJson/', views.GroupList_Json.as_view(), name="group_Json"),
    path('group/create/', views.GroupCreateView.as_view(), name="group-create"),
    path('group/<int:pk>/update/', views.GroupUpdateView.as_view(), name="group-update"),
    path('group/<int:pk>/delete/', views.GroupDeleteView.as_view(), name="group-delete"),
    path('group/<int:pk>/permissions/', views.GroupPermissionsView.as_view(), name="group-permissions"),
]