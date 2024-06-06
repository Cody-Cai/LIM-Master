from django.urls import path
from . import views
from authentication.views import UserCreateView

app_name = "system"
urlpatterns = [
    path('', views.IndexView.as_view(), name='system'),
    path('starter', views.starterView.as_view(), name='starter'),
    path('language/', views.LanguageListView.as_view(), name="language"),
    path('language/create/', views.LanguageCreateView.as_view(), name="language-create"),
    path('languagejson/', views.LanguageList_Json.as_view(), name="language-json"),
    path('langjson/', views.Language_Json.as_view(), name="langinfojson"),
    path('language/<int:pk>/update/', views.LanguageUpdateView.as_view(), name="language-update"),
    path('language/<int:pk>/delete/', views.LanguageDeleteView.as_view(), name="language-delete"),
    path('menu/', views.MenuListView.as_view(), name="menu"),
    path('menu/create/', views.MenuCreateView.as_view(), name="menu-create"),
    path('menujson/', views.MenuList_Json.as_view(), name="menu-json"),
    path('menu/<int:pk>/update/', views.MenuUpdateView.as_view(), name="menu-update"),
    path('menu/<int:pk>/delete/', views.MenuDeleteView.as_view(), name="menu-delete"),
    path('menu/<int:pk>/langtext/', views.manage_menulangname, name="menu-langText"),
    path('permission/', views.PermissionistView.as_view(), name="permission"),
    path('permissionjson/', views.PermissionList_Json.as_view(), name="permission-json"),
    path('permission/create/', views.PermissionCreateView.as_view(), name="permission-create"),
    path('permission/<int:pk>/update/', views.PermissionUpdateView.as_view(), name="permission-update"),
    path('permission/<int:pk>/delete/', views.PermissionDeleteView.as_view(), name="permission-delete"),
    path('session/', views.SessionListView.as_view(), name="session"),
    path('sessionjson/', views.SessionList_Json.as_view(), name="session-json"),
    path('session/<str:pk>/delete/', views.SessionDeleteView.as_view(), name="session-delete"),
    path('session/delete/<str:pks>', views.delete_SessionView.as_view(), name="delete-session"),
]
