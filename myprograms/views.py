from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404 as G404
from .models import ProgramPage as Pp
from .models import MyProgram as Mp
from .models import RandomizerItems as Ri
from jobs.models import Pageitem as P
from webapp.settings import LANGUAGES as L
from special.classes import PageLoad


# Strona z programami do ściągnięcia/przetestowania.
def download(request):
    if request.method == 'POST':
        pass
    else:
        pl = PageLoad(P, L)
        pl.showroom(Pp, Mp)
        context = {'items': pl.items,
                   'langs': pl.langs,
                   'pritems': pl.pritems,
                   'myprogs': pl.myprogs, }
        return render(request, 'myprograms/download.html', context)


# Strona ze szczegółami konkretnego programu.
def progpage(request, place):
    pl = PageLoad(P, L)
    pl.showroom(Pp, Mp, G404=G404, place=place)
    context = {'items': pl.items,
               'langs': pl.langs,
               'pritems': pl.pritems,
               'myprog': pl.myprog, }
    return render(request, 'myprograms/progpage.html', context)


# Emulator randomizera. Bo nie da rady tego po prostu "wygenerować".
def pybrun(request):
    if request.method == 'POST':
        pass
    else:
        pl = PageLoad(P, L)
        pl.launcher(Randomizer=Ri)
        context = {'items': pl.items,
                   'langs': pl.langs,
                   'rand': pl.randitem,
                   }
        return render(request, 'myprograms/pybrun.html', context)


# Launchpad dla wszystkich programów.
def launchme(request, place):
    if place == 1:
        return redirect('pybrun')
    else:
        pass
