from django.shortcuts import render
from django.shortcuts import get_object_or_404 as G404
from .models import Trick as Tr
from .models import Tech as Te
from blog.models import Blog as B
from myprograms.models import MyProgram
from .models import Pageitem as P
from webapp.settings import LANGUAGES as L
from webapp.special.classes import PageLoad


def home(request):
    pl = PageLoad(P, L)
    pl.portal(B=B, Tr=Tr)
    context = {'items': pl.items,
               'langs': pl.langs,
               'tricks': pl.tricks, }
    return render(request, 'tricks/home.html', context)


def newsletter(request):
    pl = PageLoad(P, L)
    pl.portal(B=B, Tr=Tr, Te=Te)
    prog = list(MyProgram.objects.all())
    news = list(B.objects.all())
    slot1 = news[-1]
    slot2 = news[-2]
    slot3 = prog[-1]
    context = {'items': pl.items,
               'langs': pl.langs,
               'tricks': pl.tricks,
               'techs': pl.techs,
               'blogs': pl.blogs,
               'dblog': slot1,
               'cblog': slot2,
               'bblog': slot3, }
    return render(request, 'tricks/newsletter.html', context)


def books(request, tricks_id):
    pl = PageLoad(P, L)
    pl.portal(Tr=Tr, G404=G404, tricksid=tricks_id)
    context = {'items': pl.items,
               'langs': pl.langs,
               'trick': pl.trick, }
    return render(request, 'tricks/books.html', context)


def skills(request, techs_id):
    pl = PageLoad(P, L)
    pl.portal(Te=Te, G404=G404, techsid=techs_id)
    context = {'items': pl.items,
               'langs': pl.langs,
               'tech': pl.tech, }
    return render(request, 'techs/skills.html', context)
