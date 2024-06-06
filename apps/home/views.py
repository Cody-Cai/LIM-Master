from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse, reverse_lazy, resolve
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from system.models import Menu
from django.shortcuts import render
# Create your views here.


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        #print(request.path_info)
        match  = resolve(request.path_info)
        # print(match.url_name)
        # print(match.app_name)
        # print(match.view_name)
        menu_nav = Menu.objects.filter(menutype="N")
        menu_top = Menu.objects.get(url='home')
        menu_side = Menu.objects.filter(parent = menu_top)
        menu_home = menu_side.filter(is_home=True)[0]
        # for menu in menu_home:
        print(menu_home.url)

        context = {
            'menu_nav': menu_nav,
            'menu_side': menu_side,
            'menu_home': menu_home,
        }
        return render(request, 'home/ihome.html', context=context)

@login_required
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/ihome.html')
    #return HttpResponse(html_template.render(context, request))
    return HttpResponse(html_template.render(context, request))
    #return render(request, 'home/starter.html')
    #return HttpResponse("Hello, world. You're at the polls index.")

@login_required
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        #load_template = request.path.split('/')[-1]
        load_template = 'starter.html'
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        return request.path
        # html_template = loader.get_template('home/page-404.html')
        # return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('home/page-500.html')
    #     return HttpResponse(html_template.render(context, request))