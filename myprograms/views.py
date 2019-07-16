from django.shortcuts import render
from django.shortcuts import get_object_or_404 as G404
from .models import MyProgram as M
from .models import ProgramPage as Pp
from jobs.models import Pageitem as P
from webapp.settings import LANGUAGES as L
from special.classes import PageLoad


# Strona z programami do ściągnięcia/przetestowania.
def download(request):
    if request.method == 'POST':
        pass
    else:
        pl = PageLoad(P, L)
        pl.showroom(M, Pp)
        context = {'items': pl.items,
                   'langs': pl.langs,
                   'myprogs': pl.myprogs,
                   'pritems': pl.pritems, }
        return render(request, 'myprogram/download.html', context)


# Strona ze szczegółami konkretnego programu.
def progpage(request, myprogram_id):
    pl = PageLoad(P, L)
    pl.showroom(M, Pp, G404=G404, myprogramid=myprogram_id)
    context = {'items': pl.items,
               'langs': pl.langs,
               'myprog': pl.myprog,
               'pritems': pl.pritems, }
    return render(request, 'myprogram/progpage.html', context)


# Emulator randomizera. Bo nie da rady tego po prostu "wygenerować".
def pybrun(request):
    if request.method == 'POST':
        pass
    else:
        pl = PageLoad(P, L)
        context = {'items': pl.items,
                   'langs': pl.langs, }
        return render(request, 'myprogram/pybrun.html', context)
