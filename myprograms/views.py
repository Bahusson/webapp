from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404 as G404
from .models import ProgramPage as Pp
from .models import MyProgram as Mp
from .models import RandomizerItems as Ri
from jobs.models import Pageitem as P
from webapp.settings import LANGUAGES as L
from special.classes import Showroom
from .management.randomize import Dataframe, randomroll
from django.http import JsonResponse


# Strona z programami do ściągnięcia/przetestowania.
def download(request):
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


# Strona Randomizera. Podobne idą do innych programów.
def pybrun(request):
    if request.method == 'POST':
        r_df = Dataframe(request)
        if r_df.no_rolls == 1:
            rows = ''
        else:
            if r_df.all_data == 1:
                rows = r_df.searchall()
            else:
                rows = r_df.returndate()
        extr = r_df.extremes()
        mode = r_df.modals()
        avg = r_df.giveaverage()
        graph = r_df.givegraph()
        responsedata = {
            'extremes': extr,
            'modals': mode,
            'average': avg,
            'graph': graph,
            'rows': rows,
        }
        return JsonResponse(responsedata)
    else:
        sh = Showroom(P, L)
        sh.randomizer(Randomizer=Ri)
        context = {'items': sh.items,
                   'langs': sh.langs,
                   'rand': sh.randitem,
                   }
        return render(request, 'myprograms/pybrun.html', context)


# Przycisk Randomizera "Zagraj".
def roll(request):
    if request.method == 'POST':
        rolls = randomroll(request)
        responsedata = {
            'numbers': rolls
        }
        return JsonResponse(responsedata)


# Launchpad dla wszystkich programów. Rozszerzasz tylko redlistę o nazwy def.
def launchme(request, place):
    redlist = ['pybrun', ]
    return redirect(redlist[place-1])
