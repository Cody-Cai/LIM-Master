from django.urls import path
from . import views


app_name = "vend"
urlpatterns = [
    path('setup/vendgroup/', views.VendGroupListView.as_view(), name="vendgroup"),
    path('setup/vendgroup/create/', views.VendGroupCreateView.as_view(), name="vendgroup-create"),
    path('setup/vendgroupjson/', views.VendGroup_Json.as_view(), name="vendgroup-json"),
    path('setup/vendgroup/<int:pk>/update/', views.VendGroupUpdateView.as_view(), name="vendgroup-update"),
    path('setup/vendgroup/<int:pk>/delete/', views.VendGroupDeleteView.as_view(), name="vendgroup-delete"),
    path('vendtable/', views.VendTableListView.as_view(), name="vendtable"),
    path('vendtable/create/', views.VendTableCreateView.as_view(), name="vendtable-create"),
    path('vendtable/<int:pk>/update/', views.VendTableUpdateView.as_view(), name="vendtable-update"),
    path('vendtablejson/', views.VendTable_Json.as_view(), name="vendtable-json"),
    path('vendtable/<int:pk>/delete/', views.VendTableDeleteView.as_view(), name="vendtable-delete"),
    path('vendtable/vendaddress/<int:vendtable_id>/create/', views.VendAddressCreateView.as_view(), name="vendaddress-create"),
    path('vendtable/vendaddress/<int:pk>/update/', views.VendAddressUpdateView.as_view(), name="vendaddress-update"),
    path('vendtable/vendaddress/<int:pk>/delete/', views.VendAddressDeleteView.as_view(), name="vendaddress-delete"),
    path('vendtable/vendaddress/<int:pk>/', views.VendAddressDetailView.as_view(), name="vendaddress-detail"),
    path('vendtable/vendcontact/<int:vendtable_id>/create/', views.VendContactCreateView.as_view(), name="vendcontact-create"),
    path('vendtable/vendcontact/<int:pk>/update/', views.VendContactUpdateView.as_view(), name="vendcontact-update"),
    path('vendtable/vendcontact/<int:pk>/delete/', views.VendContactDeleteView.as_view(), name="vendcontact-delete"),
    path('vendtable/vendcontact/<int:pk>/', views.VendContactDetailView.as_view(), name="vendcontact-detail"),
]