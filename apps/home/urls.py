from django.urls import path, re_path

from apps.home import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('starter', views.pages, name='pages'),
    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),
]