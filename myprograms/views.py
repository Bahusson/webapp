from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404 as G404
from .models import ProgramPage as Pp
from .models import MyProgram as Mp
from .models import RandomizerItems as Ri
from jobs.models import Pageitem as P
from webapp.settings import LANGUAGES as L
from special.classes import Showroom
from .management.randomize import Database, Dataframe
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
        r_db = Database(request)
        r_df = Dataframe(request)
        extr = ''
        mode = ''
        dtfr = ''

        if r_db.no_rolls == 1:
            rows = ''
        else:
            if r_db.all_data == 1:
                rows = r_db.searchall()
            else:
                rows = r_db.selectdate()
        if r_db.extreme_nums or r_db.mode == 1:
            ext = r_df.extremes()
            extr = getattr(ext, 'extr', '')
            mode = getattr(ext, 'modals', '')
        if r_db.av_score == 1:  # OR r_db.gen_graph //
            dfr = r_df.makedf()
            dtfr = getattr(dfr, 'average', '')
        responsedata = {
            'rows': rows,
            'extremes': extr,
            'modals': mode,
            'average': dtfr
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


# Launchpad dla wszystkich programów. Rozszerzasz tylko listę o nazwy def.
def launchme(request, place):
    redlist = ['pybrun', ]
    return redirect(redlist[place-1])
