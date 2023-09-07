from django.conf import settings

def cfg_assets_root(request):
    print(settings.ASSETS_ROOT)
    return { 'ASSETS_ROOT' : settings.ASSETS_ROOT }