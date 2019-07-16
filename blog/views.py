from django.shortcuts import render
from django.shortcuts import get_object_or_404 as G404
from .models import Blog as B
from .models import Pageitem as P
from webapp.settings import LANGUAGES as L
from webapp.special.classes import PageLoad


# Zestawienie wszystkich wpisów na blogu.
def allblogs(request):
    pl = PageLoad(P, L)
    pl.portal(B=B)
    context = {'items': pl.items,
               'langs': pl.langs,
               'blogs': pl.blogs, }
    return render(request, 'blog/allblogs.html', context)


# Pełna strona konkretnego wpisu na blogu.
def detail(request, blog_id):
    pl = PageLoad(P, L)
    pl.portal(B=B, G404=G404, blogid=blog_id)
    context = {'items': pl.items,
               'langs': pl.langs,
               'blog': pl.blog, }
    return render(request, 'blog/detail.html', context)
