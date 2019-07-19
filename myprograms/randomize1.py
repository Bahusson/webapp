from django.http import JsonResponse, HttpResponse
import psycopg2
import pandas
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource
import re
import configparser
import datetime
from special.snippets import bug_catch


class Database(object):

    def __init__(self, db):
        self.conn = psycopg2.connect(db)
        self.cur = self.conn.cursor()

    def selector(
         self, base, table, day1, month1, year1, day2, month2, year2, q, ):
        if q == 1:
            duck = '<='
            quack = ">="
        elif q == 0:
            duck = '='
            quack = '='
        if base == 4 or 8:
            range = "1"
            execall = 'SELECT "2", "3", "4", "5", "6", "7", "8", "9", "10" FROM %s LIMIT %s OFFSET %s', (
             table, rowto, rowfrom, )
        else:
            range = "0"
            execall = 'SELECT * FROM %s LIMIT %s OFFSET %s', (
             table, rowto, rowfrom, )
        self.cur.execute(
         'SELECT MIN(%s) FROM %s WHERE "2" %s %s AND "3"=%s AND "4"=%s', (
          range, table, duck, day2, month2, year2, ))
        self.rowfrom = (self.cur.fetchone()[0])
        self.cur.execute(
         'SELECT MAX(%s) FROM %s WHERE "2" %s %s AND "3"=%s AND "4"=%s', (
          range, table, quack, day1, month1, year1, ))
        self.rowfrom = (self.cur.fetchone()[0])
        self.cur.execute(execall)
        self.rows = self.cur.fetchall()
        self.conn.close()


# Główna oś funkcji
def generate(request):
    global radio
    global datal
    global nhilo
    global norol
    global moftn
    global avsco
    global grgen
    global rad
    global datfro
    global dattoo
    global table
    if request.is_ajax():
        radio = request.POST.get('gamesel')
        datfr = re.findall(r"(\d\d\d\d)-(\d\d)-(\d\d)",
                           request.POST['datefrom'])
        datto = re.findall(r"(\d\d\d\d)-(\d\d)-(\d\d)",
                           request.POST['dateto'])
        datal = request.POST['dateall']
        nhilo = request.POST['numhilow']
        norol = request.POST['norolls']
        moftn = request.POST['mostoften']
        avsco = request.POST['avgscores']
        grgen = request.POST['graphgen']

        table = "game" + radio

        if datal == "0":
            datfro = datfr[0]
            dattoo = datto[0]
            allrollstrigger = False
        elif datal == "1":
            allrollstrigger = True
        else:
            bug_catch()

    radparam()

    if datal == '1':
        searchallbox(radio)
    else:
        pass

    enumerators(rad, moftn, nhilo, )
    makedf(rad, avsco, grgen, )

    if norol == '1':
        rolls = "Nie wybrano losowań"
    elif norol == "0" and datal == "0":
        rollhead = ["Losowania wraz z datą:" + "\n"]
        rowspacing = list()
        while len(rowspacing) < len(rows):
            rowspacing.append("\n")
        zippedrows = zip(rows, rowspacing, )
        ziprows = list(zippedrows)
        rolls = [rollhead, ziprows, ]
    elif norol == "0" and datal == "1":
        rolls = "Zaznaczono całość pomiarów"
    else:
        bug_catch()

    responsedata = {
        'hilow': hilow,
        'rolls': rolls,
        'often': often,
        'avgsc': avgsc,
        # Co do ostatniego to możliwe, że trzeba będzie dodaĆ
        # warunkowe return/render HttpResponse pod ten graf.
        'graph': graph
    }
    return JsonResponse(responsedata)


# Można uży tej funkcji do uporządkowania spraw
# z backendem tak żeby go nie przepisywać w całości.
# To fukcja przypisująca numery od 1 do 8 w zależności od
# przypadku bazy danych i tego czy
# jest filtrowana czy nie.
def radparam():
    global rad
    if datal + radio == "11":
        rad = 1
    elif datal + radio == "12":
        rad = 2
    elif datal + radio == "13":
        rad = 3
    elif datal + radio == "14":
        rad = 4
    elif datal + radio == "01":
        rad = 5
        searchA(
                1, dattoo[2], dattoo[1], dattoo[0],
                datfro[2], datfro[1], datfro[0], )
    elif datal + radio == "02":
        rad = 6
        searchA(
                2, dattoo[2], dattoo[1], dattoo[0],
                datfro[2], datfro[1], datfro[0], )
    elif datal + radio == "03":
        rad = 7
        searchA(
                3, dattoo[2], dattoo[1], dattoo[0],
                datfro[2], datfro[1], datfro[0], )
    elif datal + radio == "04":
        rad = 8
        searchA(
                4, dattoo[2], dattoo[1], dattoo[0],
                datfro[2], datfro[1], datfro[0], )

    else:
        pass


# Ta funkcja ogranicza bazę rakordów do konkretnych dat.
def searchA(base, day1, month1, year1, day2, month2, year2, ):
    conn = psycopg2.connect("dbname=webappbasedb user=postgres password=Ma3taksamo_Jakja")
    cur = conn.cursor()
    global rowfrom
    global rowto
    global rows
    if base == 1:
        cur.execute('SELECT MIN("0") FROM game1 WHERE "2"=%s AND "3"=%s AND "4"=%s',(day2,month2,year2))
        rowfrom=(cur.fetchone()[0])
        cur.execute('SELECT MAX("0") FROM game1 WHERE "2"=%s AND "3"=%s AND "4"=%s',(day1,month1,year1))
        rowto=(cur.fetchone()[0])-rowfrom
        cur.execute('SELECT * FROM game1 LIMIT %s OFFSET %s', (rowto, rowfrom))
    elif base == 2:
        cur.execute('SELECT MAX("0") FROM game2 WHERE "2"<=%s AND "3"=%s AND "4"=%s',(day2,month2,year2))
        rowfrom=(cur.fetchone()[0])
        cur.execute('SELECT MIN("0") FROM game2 WHERE "2">=%s AND "3"=%s AND "4"=%s',(day1,month1,year1))
        rowto=(cur.fetchone()[0])-rowfrom
        cur.execute('SELECT * FROM game2 LIMIT %s OFFSET %s', (rowto, rowfrom))
    elif base == 3:
        cur.execute('SELECT MAX("0") FROM game3 WHERE "2"<=%s AND "3"=%s AND "4"=%s',(day2,month2,year2))
        rowfrom=(cur.fetchone()[0])
        cur.execute('SELECT MIN("0") FROM game3 WHERE "2">=%s AND "3"=%s AND "4"=%s',(day1,month1,year1))
        rowto=(cur.fetchone()[0])-rowfrom
        cur.execute('SELECT * FROM game3 LIMIT %s OFFSET %s', (rowto, rowfrom))
    elif base == 4:
        cur.execute('SELECT MIN("1") FROM game4 WHERE "2"=%s AND "3"=%s AND "4"=%s',(day2,month2,year2))
        rowfrom=(cur.fetchone()[0])
        cur.execute('SELECT MAX("1") FROM game4 WHERE "2"=%s AND "3"=%s AND "4"=%s',(day1,month1,year1))
        rowto=(cur.fetchone()[0])-rowfrom
        cur.execute('SELECT "2", "3", "4", "5", "6", "7", "8", "9", "10" FROM game4 LIMIT %s OFFSET %s', (rowto, rowfrom))
    rows=cur.fetchall()
    conn.close()

#Funkcja searchall dla checkboxa ściągająca dane z całej bazy danych. .
def searchallbox(var):
    conn=psycopg2.connect("dbname=webappbasedb user=postgres password=Ma3taksamo_Jakja")
    cur=conn.cursor()
    if var == "1" :
        cur.execute('SELECT * FROM game1')
    elif var == "2" :
        cur.execute('SELECT * FROM game2')
    elif var == "3" :
        cur.execute('SELECT * FROM game3')
    elif var == "4" :
        cur.execute('SELECT "2", "3", "4", "5", "6", "7", "8", "9", "10" FROM game4')
    rows=cur.fetchall()
    conn.close()
#    return rows

#Ta podfunkcja wywołuje graf Bokeh.
def makegraph():
        p=figure(plot_width=500, plot_height=400, tools = 'pan, reset', logo=None)
        p.title.text = "Dystrybucja"
        p.title.text_color = "Orange"
        p.title.text_font = "times"
        p.title.text_font_style = "italic"
        p.yaxis.minor_tick_line_color = "Yellow"
        p.xaxis.axis_label = "Średnie"
        p.yaxis.axis_label = "Częstotliwości"
        p.circle(x='Means', y='Freqs', source=source, size = 10, color="red", alpha=0.6)
        hover=HoverTool(tooltips=[("Mean","@Means"),("Freq","@Freqs")])
        p.add_tools(hover)
        output_file('graph1.html')
        show(p)

#Ta podfunkcja rekonwertująca bazę danych do df aby można było zrobić graf i inne fajne rzeczy na liczbach...
def dfdb(var):
    global df
    if var == 1 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game1'),
            con=psycopg2.connect("dbname=webappbasedb user=postgres password=Ma3taksamo_Jakja"), coerce_float=False, parse_dates=None, chunksize=None)
    elif var == 2 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game2'),
            con=psycopg2.connect("dbname=webappbasedb user=postgres password=Ma3taksamo_Jakja"), coerce_float=False, parse_dates=None, chunksize=None)
    elif var == 3 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game3'),
            con=psycopg2.connect("dbname=webappbasedb user=postgres password=Ma3taksamo_Jakja"), coerce_float=False, parse_dates=None, chunksize=None)
    elif var == 4 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game4'),
            con=psycopg2.connect("dbname=webappbasedb user=postgres password=Ma3taksamo_Jakja"), coerce_float=False, parse_dates=None, chunksize=None)
    elif var == 5 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game1 LIMIT %s OFFSET %s'),
            con=psycopg2.connect("dbname=webappbasedb user=postgres password=Ma3taksamo_Jakja"), coerce_float=False, params=[rowto, rowfrom], parse_dates=None, chunksize=None)
    elif var == 6 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game2 LIMIT %s OFFSET %s'),
            con=psycopg2.connect("dbname=webappbasedb user=postgres password=Ma3taksamo_Jakja"), coerce_float=False, params=[rowto, rowfrom], parse_dates=None, chunksize=None)
    elif var == 7 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game3 LIMIT %s OFFSET %s'),
            con=psycopg2.connect("dbname=webappbasedb user=postgres password=Ma3taksamo_Jakja"), coerce_float=False, params=[rowto, rowfrom], parse_dates=None, chunksize=None)
    elif var == 8 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game4 LIMIT %s OFFSET %s'),
            con=psycopg2.connect("dbname=webappbasedb user=postgres password=Ma3taksamo_Jakja"), coerce_float=False, params=[rowto, rowfrom], parse_dates=None, chunksize=None)

#Zwraca najwyższą, najniższą liczbę, oraz liczby od najczęstszej.
def enumerators(base,value,var1):
    dfdb(base)
    global hilow
    global often
    if base == 4 or base == 8 :
        df1=df.drop(df.columns[0:4],1)
        df1=df1.drop(df.columns[-1],1)
    else:
        df1=df.drop(df.columns[0:5],1)
    df2 = df1.apply(pandas.value_counts).fillna(0);
    df2.loc[:,'total'] = df2.sum(axis=1)
    df3=df2
    nplus = df3.sort_values(['total'], ascending=[False])[:1].index.values;
    nminus = df3.sort_values(['total'], ascending=[False])[-1:].index.values;
    nums = df3.sort_values(['total'], ascending=[False])[:int(value)].index.values;

    if var1 == '1':
        hilow = "Max: " + str(nplus) + "  Min: " + str(nminus)
    else:
        hilow = "Nie wybrano liczb skrajnych"
    if int(value) > 0 :
        often = "Od najczęstszej: " + str(nums)
    else: "Nie wybrano najczęstszych liczb"

#Nadfunkcja - Zwraca graf i średnie wyników losowań.
def makedf(base,var1,var2):
    dfdb(base)
    global df1
    global graph
    global source
    global avgsc
    if base == 4 or base == 8 :
        df1=df.drop(df.columns[0:4],1)
        df1=df1.drop(df.columns[-1],1)
    else:
        df1=df.drop(df.columns[0:3],1)
    df4=df1.T
    df5=df4.mean().round(0).value_counts()
    slist = list()
    nrlist = list()
    while len(slist)<len(df5.index):
        slist.append(" / ")
    while len(nrlist)<len(df5.index):
        nrlist.append("\n")
    dfindex = df5.index.astype(str)
    dfvalue = df5.values.astype(str)
    zipped = zip(dfindex, slist, dfvalue, nrlist)
    a=list(zipped)
    ahead= ["Średnia" + " / " + "Częstotliwość" + "\n" ]
    b=ahead+a

    source = ColumnDataSource(
        data=dict(
            Means=df5.index,
            Freqs=df5.values
            ))
    if var1 == '1' and var2 == '1':
            makegraph()
            avgsc = b
    elif var1 == '0' and var2 == '1':
            makegraph()
            avgsc = "Nie wybrano generowania średnich"
    elif var1 == '1' and var2 == '0':
            avgsc = b
            graph = "Nie wybrano generowania wykresu"
    else:
            avgsc = "Nie wybrano generowania średnich"
            graph = "Nie wybrano generowania wykresu"

#Ta funkcja wyciąga z bazy danych pierwszą/ostatnią datę. (W wersji webowej do zaimplementowania na końcu...)
def getcaldate(base, date):
    conn=psycopg2.connect("dbname=webappbasedb user=postgres password=Ma3taksamo_Jakja")
    cur=conn.cursor()
    if base == 1 and date == 1 :
        cur.execute('SELECT "2","3","4" FROM game1 ORDER BY rowid ASC LIMIT 1')
    elif base == 2 and date == 1 :
        cur.execute('SELECT "2","3","4" FROM game2 ORDER BY rowid ASC LIMIT 1')
    elif base == 3 and date == 1 :
        cur.execute('SELECT "2","3","4" FROM game3 ORDER BY rowid ASC LIMIT 1')
    elif base == 4 and date == 1 :
        cur.execute('SELECT "2","3","4" FROM game4 ORDER BY rowid ASC LIMIT 1')
    elif base == 1 and date == 2 :
        cur.execute('SELECT "2","3","4" FROM game1 ORDER BY rowid DESC LIMIT 1')
    elif base == 2 and date == 2 :
        cur.execute('SELECT "2","3","4" FROM game2 ORDER BY rowid DESC LIMIT 1')
    elif base == 3 and date == 2 :
        cur.execute('SELECT "2","3","4" FROM game3 ORDER BY rowid DESC LIMIT 1')
    elif base == 4 and date == 2 :
        cur.execute('SELECT "2","3","4" FROM game4 ORDER BY rowid DESC LIMIT 1')
    rows=cur.fetchall()
    conn.close()
    #return rows
