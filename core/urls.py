"""
URL configuration for lim_master project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path("", include("apps.authentication.urls")), # Auth routes - login / register
    path('', include('apps.authentication.urls')),
    path('', include('apps.home.urls')),
    path('system/', include('apps.system.urls')),
    path('basic/', include('apps.basic.urls')),
    path('hrm/', include('apps.hrm.urls')),
    path("i18n/", include("django.conf.urls.i18n")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handling the 404 error
handler404 = "apps.system.views.error_404_view"

handler500 = "apps.system.views.error_500_view"

handler403 = "apps.system.views.error_403_view"