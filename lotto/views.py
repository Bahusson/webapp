from django.contrib.auth.models import User, Group
#from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
import importlib
from .models import Lotto

def download(request):
    if request.method == 'GET':
        lots = Lotto.objects
        return render(request, 'lotto/download.html', {'lots':lots})

#Ta funkcja kieruje na podstronę ze szczegółami wybranego programu.
def progpage(request, lotto_id):
    detprog = get_object_or_404(Lotto, pk=lotto_id)
    return render(request, 'lotto/progpage.html', {'lotto': detprog})

def pybrun (request):
    if request.method == 'GET':
        return render(request, 'lotto/pybrun.html')
