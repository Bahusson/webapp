from django.shortcuts import render
from django.shortcuts import get_object_or_404 as G404
from .models import Blog as B
from jobs.models import Pageitem as P
from webapp.settings import LANGUAGES as L
from special.classes import Blog

bl = Blog(P, L)


# Zestawienie wszystkich wpisów na blogu.
def allblogs(request):
    bl.gen(B=B)
    context = {'items': bl.items,
               'langs': bl.langs,
               'blogs': bl.blogs, }
    return render(request, 'blog/allblogs.html', context)


# Pełna strona konkretnego wpisu na blogu.
def detail(request, blog_id):
    bl.gen(B=B, G404=G404, blogid=blog_id)
    context = {'items': bl.items,
               'langs': bl.langs,
               'blog': bl.blog, }
    return render(request, 'blog/detail.html', context)
