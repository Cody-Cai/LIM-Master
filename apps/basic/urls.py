from django.urls import path
from . import views


app_name = "basic"
urlpatterns = [
    path('setup/country/', views.CountryListView.as_view(), name="country"),
    path('setup/country/create/', views.CountryCreateView.as_view(), name="country-create"),
    path('setup/countryjson/', views.CountryList_Json.as_view(), name="country-json"),
    path('setup/country/<int:pk>/update/', views.CountryUpdateView.as_view(), name="country-update"),
    path('setup/country/<int:pk>/delete/', views.CountryDeleteView.as_view(), name="country-delete"),
    path('setup/currency/', views.CurrencyListView.as_view(), name="currency"),
    path('setup/currency/create/', views.CurrencyCreateView.as_view(), name="currency-create"),
    path('setup/currencyjson/', views.CurrencyList_Json.as_view(), name="currency-json"),
    path('setup/currency/<int:pk>/update/', views.CurrencyUpdateView.as_view(), name="currency-update"),
    path('setup/currency/<int:pk>/delete/', views.CurrencyDeleteView.as_view(), name="currency-delete"),
    path('company/', views.CompanyInfoView.as_view(), name="company"),
    path('setup/companyaddress/<int:pk>/create/', views.create_companyaddress, name="companyaddress-create"),
    path('setup/companyaddress/<int:pk>/update/', views.update_companyaddress, name="companyaddress-update"),
    path('setup/companyaddress/<int:pk>/delete/', views.delete_companyaddress, name="companyaddress-delete"),
    path('setup/companyaddress/<int:pk>/', views.detail_companyaddress, name="companyaddress-detail"),
    path('setup/unit/', views.UnitListView.as_view(), name="unit"),
    path('setup/unit/create/', views.UnitCreateView.as_view(), name="unit-create"),
    path('setup/unitjson/', views.Unit_Json.as_view(), name="unit-json"),
    path('setup/unit/<int:pk>/update/', views.UnitUpdateView.as_view(), name="unit-update"),
    path('setup/unit/<int:pk>/delete/', views.UnitDeleteView.as_view(), name="unit-delete"),
    path('setup/unit/<int:pk>/unittext/', views.manage_unittext, name="unit-text"),
    path('setup/unitconvert/', views.UnitConvertListView.as_view(), name="unitconvert"),
    path('setup/unitconvert/create/', views.UnitConvertCreateView.as_view(), name="unitconvert-create"),
    path('setup/unitconvertjson/', views.UnitConvert_Json.as_view(), name="unitconvert-json"),
    path('setup/unitconvert/<int:pk>/update/', views.UnitConvertUpdateView.as_view(), name="unitconvert-update"),
    path('setup/unitconvert/<int:pk>/delete/', views.UnitConvertDeleteView.as_view(), name="unitconvert-delete"),
    path('setup/numbersequence/', views.NumberSequenceTableListView.as_view(), name="numbersequence"),
    path('setup/numbersequence/create/', views.NumberSequenceTableCreateView.as_view(), name="numbersequence-create"),
    path('setup/numbersequencejson/', views.NumberSequenceTable_Json.as_view(), name="numbersequence-json"),
    path('setup/numbersequence/<int:pk>/update/', views.NumberSequenceTableUpdateView.as_view(), name="numbersequence-update"),
    path('setup/numbersequence/<int:pk>/delete/', views.NumberSequenceTableDeleteView.as_view(), name="numbersequence-delete"),
]