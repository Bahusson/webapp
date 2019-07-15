from django.shortcuts import render, get_object_or_404
from .models import MyProgram


def download(request):
    if request.method == 'GET':
        lots = MyProgram.objects
        return render(request, 'myprogram/download.html', {'lots': lots})


# Ta funkcja kieruje na podstronę ze szczegółami wybranego programu.
def progpage(request, myprogram_id):
    detprog = get_object_or_404(MyProgram, pk=myprogram_id)
    return render(request, 'myprogram/progpage.html', {'myprogram': detprog})


def pybrun(request):
    if request.method == 'GET':
        return render(request, 'myprogram/pybrun.html')
