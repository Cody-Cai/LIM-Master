from django.urls import path
from . import views


app_name = "basic"
urlpatterns = [
    path('seting/country/', views.CountryListView.as_view(), name="country"),
    path('seting/country/create/', views.CountryCreateView.as_view(), name="country-create"),
    path('seting/countryjson/', views.CountryList_Json.as_view(), name="country-json"),
    path('seting/country/<int:pk>/update/', views.CountryUpdateView.as_view(), name="country-update"),
    path('seting/country/<int:pk>/delete/', views.CountryDeleteView.as_view(), name="country-delete"),
    path('seting/currency/', views.CurrencyListView.as_view(), name="currency"),
    path('seting/currency/create/', views.CurrencyCreateView.as_view(), name="currency-create"),
    path('seting/currencyjson/', views.CurrencyList_Json.as_view(), name="currency-json"),
    path('seting/currency/<int:pk>/update/', views.CurrencyUpdateView.as_view(), name="currency-update"),
    path('seting/currency/<int:pk>/delete/', views.CurrencyDeleteView.as_view(), name="currency-delete"),
    path('company/', views.CompanyInfoView.as_view(), name="company"),
    path('seting/companyaddress/<int:pk>/create/', views.create_companyaddress, name="companyaddress-create"),
    path('seting/companyaddress/<int:pk>/update/', views.update_companyaddress, name="companyaddress-update"),
    path('seting/companyaddress/<int:pk>/delete/', views.delete_companyaddress, name="companyaddress-delete"),
    path('seting/companyaddress/<int:pk>/', views.detail_companyaddress, name="companyaddress-detail"),
]