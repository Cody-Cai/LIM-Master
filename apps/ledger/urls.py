from django.urls import path
from . import views


app_name = "ledger"
urlpatterns = [
    path('setup/taxtable/', views.TaxTableListView.as_view(), name="taxtable"),
    path('setup/taxtable/create/', views.TaxTableCreateView.as_view(), name="taxtable-create"),
    path('setup/taxtablejson/', views.TaxTable_Json.as_view(), name="taxtable-json"),
    path('setup/taxtable/<int:pk>/update/', views.TaxTableUpdateView.as_view(), name="taxtable-update"),
    path('setup/taxtable/<int:pk>/delete/', views.TaxTableDeleteView.as_view(), name="taxtable-delete"),
    path('setup/taxgroupheading/', views.TaxGroupHeadingListView.as_view(), name="taxgroupheading"),
    path('setup/taxgroupheading/create/', views.TaxGroupHeadingCreateView.as_view(), name="taxgroupheading-create"),
    path('setup/taxgroupheadingjson/', views.TaxGroupHeading_Json.as_view(), name="taxgroupheading-json"),
    path('setup/taxgroupheading/<int:pk>/update/', views.TaxGroupHeadingUpdateView.as_view(), name="taxgroupheading-update"),
    path('setup/taxgroupheading/<int:pk>/delete/', views.TaxGroupHeadingDeleteView.as_view(), name="taxgroupheading-delete"),
    path('setup/taxitemgroupheading/', views.TaxItemGroupHeadingListView.as_view(), name="taxitemgroupheading"),
    path('setup/taxitemgroupheading/create/', views.TaxItemGroupHeadingCreateView.as_view(), name="taxitemgroupheading-create"),
    path('setup/taxitemgroupheadingjson/', views.TaxItemGroupHeading_Json.as_view(), name="taxitemgroupheading-json"),
    path('setup/taxitemgroupheading/<int:pk>/update/', views.TaxItemGroupHeadingUpdateView.as_view(), name="taxitemgroupheading-update"),
    path('setup/taxitemgroupheading/<int:pk>/delete/', views.TaxItemGroupHeadingDeleteView.as_view(), name="taxitemgroupheading-delete"),
]