from django.urls import path
from . import views


app_name = "hrm"
urlpatterns = [
    path('organization/', views.OrganizationUnitView.as_view(), name="organization"),
    path('organization/create/', views.OrganizationUnitCreateView.as_view(), name="organization-create"),
    path('organizationjson/', views.OrganizationUnit_Json.as_view(), name="organization-json"),
    path('organization/<int:pk>/update/', views.OrganizationUnitUpdateView.as_view(), name="organization-update"),
    path('organization/<int:pk>/delete/', views.OrganizationUnitDeleteView.as_view(), name="organization-delete"),
    path('employee/', views.EmployeeView.as_view(), name="employee"),
    path('employee/create/', views.EmployeeCreateView.as_view(), name="employee-create"),
    path('employeejson/', views.Employee_Json.as_view(), name="employee-json"),
    path('employee/<int:pk>/update/', views.EmployeeUpdateView.as_view(), name="employee-update"),
    path('employee/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name="employee-delete"),
    path('setup/persontitle/', views.PersonTitleView.as_view(), name="persontitle"),
    path('setup/persontitle/create/', views.PersonTitleCreateView.as_view(), name="persontitle-create"),
    path('setup/persontitlejson/', views.PersonTitle_Json.as_view(), name="persontitle-json"),
    path('setup/persontitle/<int:pk>/update/', views.PersonTitleUpdateView.as_view(), name="persontitle-update"),
    path('setup/persontitle/<int:pk>/delete/', views.PersonTitleDeleteView.as_view(), name="persontitle-delete"),
]