from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login  # , logout
from django.shortcuts import get_object_or_404 as G404
from .models import Curriculum as Cv
from .models import Trick as Tr
from .models import Tech as Te
from blog.models import Blog as B
from myprograms.models import MyProgram as Mp
from myprograms.models import ProgramPage as Pp
from .models import Pageitem as P
from webapp.settings import LANGUAGES as L
from special.classes import PageLoad, Trick, Blog, Tech, Showroom, CV
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


# Strona Startowa.
def home(request):
    pl = PageLoad(P, L)
    pl.gen()
    context = {'items': pl.items,
               'langs': pl.langs, }
    return render(request, 'tricks/home.html', context)


def about(request):
    pl = PageLoad(P, L)
    context = {'items': pl.items,
               'langs': pl.langs, }
    return render(request, 'tricks/about.html', context)


# Strona 'Aktualności'. Dużo różnych rzeczy - skrótowo.
def newsletter(request):
    tr = Trick(P, L)
    bl = Blog()
    te = Tech()
    pr = Showroom()
    tr.gen(Tr=Tr)
    bl.gen(B=B)
    te.gen(Te=Te)
    pr.gen(Pp=Pp, Mp=Mp)
    context = {'items': tr.items,
               'langs': tr.langs,
               'tricks': tr.tricks,
               'techs': te.techs,
               'blogs': bl.bloglist,
               'pritems': pr.pritems,
               'myprogs': pr.proglist, }
    return render(request, 'tricks/newsletter.html', context)


# Pełna strona konkretnej ciekawostki.
def books(request, tricks_id):
    tr = Trick(P, L)
    tr.gen(Tr=Tr, G404=G404, tricksid=tricks_id)
    context = {'items': tr.items,
               'langs': tr.langs,
               'trick': tr.trick, }
    return render(request, 'tricks/books.html', context)


# Pełna strona konkretnej umiejętności.
def skills(request, techs_id):
    te = Tech(P, L)
    cv = CV(Cv=Cv)
    te.gen(Te=Te, G404=G404, techsid=techs_id)
    context = {'items': te.items,
               'langs': te.langs,
               'techs': te.techs,
               'tech': te.tech,
               'cv': cv.cv, }
    return render(request, 'techs/skills.html', context)


# Formularz logowania.
def logger(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Tutaj trzeba wstawić jakiś error message.
            pass
    else:
        pl = PageLoad(P, L)
        form = AuthenticationForm()
        context = {'items': pl.items,
                   'langs': pl.langs,
                   'form': form, }
    return render(request, 'registration/login.html', context)


# Formularz rejestracji.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  # Hasło j.w.
            user = authenticate(username=username, password=password)
            login(request, user)  # Loguje usera.
            return redirect('home')
            # Przekierowuje na stronę główną zalogowanego usera.
    else:  # Zanim wyślemy cokolwiek mysimy wygenerować formularz na stronie.
        pl = PageLoad(P, L)
        form = UserCreationForm()
        context = {'items': pl.items,
                   'langs': pl.langs,
                   'form': form, }
    return render(request, 'registration/register.html', context)
