from django.http import JsonResponse
import pandas
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource

#Główna oś funkcji
def generate(request):




    responsedata = {
        'hilow' : hilow
        'rolls' : rolls
        'often' : often
        'avgsc' : avgsc
        'graph' : graph 
    }
    return JsonResponse(responsedata)
