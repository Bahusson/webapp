from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404 as G404
from .models import ProgramPage as Pp
from .models import MyProgram as Mp
from .models import RandomizerItems as Ri
from jobs.models import Pageitem as P
from webapp.settings import LANGUAGES as L
from special.classes import Showroom


# Strona z programami do ściągnięcia/przetestowania.
def download(request):
    if request.method == 'POST':
        pass
    else:
        sh = Showroom(P, L)
        sh.gen(Pp=Pp, Mp=Mp)
        context = {'items': sh.items,
                   'langs': sh.langs,
                   'pritems': sh.pritems,
                   'myprogs': sh.myprogs, }
        return render(request, 'myprograms/download.html', context)


# Strona ze szczegółami konkretnego programu.
def progpage(request, place):
    sh = Showroom(P, L)
    sh.gen(Pp=Pp, Mp=Mp, G404=G404, place=place)
    context = {'items': sh.items,
               'langs': sh.langs,
               'pritems': sh.pritems,
               'myprog': sh.myprog, }
    return render(request, 'myprograms/progpage.html', context)


# Emulator randomizera. Bo nie da rady tego po prostu "wygenerować".
def pybrun(request):
    if request.method == 'POST':
        pass
    else:
        sh = Showroom(P, L)
        sh.launcher(Randomizer=Ri)
        context = {'items': sh.items,
                   'langs': sh.langs,
                   'rand': sh.randitem,
                   }
        return render(request, 'myprograms/pybrun.html', context)


# Launchpad dla wszystkich programów.
def launchme(request, place):
    redlist = ['pybrun', ]
    return redirect(redlist[place-1])
