from django.contrib.auth.models import User, Group
#from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
import importlib
#import os
from .models import Lotto
from django.http import HttpResponse


def download(request):
    if request.method == 'GET':
        lots = Lotto.objects
        return render(request, 'lotto/download.html', {'lots':lots})
    #Wyłączona funkcja odpalająca tkinter GUI na stronie odkąd zdecydowałem się na przepisanie frontu pod web.
    #elif request.method == 'POST':
        #lots = Lotto.objects
        #os.system('python lotto/randfront.py')
        #return render(request, 'lotto/download.html', {'lots':lots})

#Ta funkcja kieruje na podstronę ze szczegółami wybranego programu.
def progpage(request, lotto_id):
    detprog = get_object_or_404(Lotto, pk=lotto_id)
    return render(request, 'lotto/progpage.html', {'lotto': detprog})

def pybrun (request):
    return render(request, 'lotto/pybrun.html')

#To funkcja frontu "zagraj w grę" pod AJAX.
def roll (request):
    if request.method == 'POST':
        radio = request.POST['radio_button_value']
        #import randomize1
        #print(lst1)
        return HttpResponse(radio)
