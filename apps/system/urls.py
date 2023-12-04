from django.urls import path
from . import views
from apps.authentication.views import UserCreateView

app_name = "system"
urlpatterns = [
    path('language/', views.LanguageListView.as_view(), name="language"),
    path('language/create/', views.LanguageCreateView.as_view(), name="language-create"),
    path('languagejson/', views.LanguageList_Json.as_view(), name="language-json"),
    path('langjson/', views.Language_Json.as_view(), name="langinfojson"),
    path('language/<int:pk>/update/', views.LanguageUpdateView.as_view(), name="language-update"),
    path('language/<int:pk>/delete/', views.LanguageDeleteView.as_view(), name="language-delete"),
]
