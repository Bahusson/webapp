from django.http import JsonResponse, HttpResponse
import psycopg2
import pandas
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource
import re
import ConfigParser
import datetime
from .managment.commands.updatedb import Updatedb
from special.snippets import bug_catch


# Żeby uniknąć zdań warunkowych wykorzystaj polimorfizm dla bazy 4!

class Database(object):

    def __init__(self, request):
        if request.is_ajax():  # Czy można bez If request is ajax?
            # Albo wyrzucić request is ajax do views?
            self.base = request.POST.get('gamesel')
            self.datfr = re.findall(r"(\d\d\d\d)-(\d\d)-(\d\d)",
                                    request.POST['datefrom'])
            self.datto = re.findall(r"(\d\d\d\d)-(\d\d)-(\d\d)",
                                    request.POST['dateto'])
            self.datal = request.POST['dateall']
            self.nhilo = request.POST['numhilow']
            self.norol = request.POST['norolls']
            self.moftn = request.POST['mostoften']
            self.avsco = request.POST['avgscores']
            self.grgen = request.POST['graphgen']
            self.table = "game" + str(self.base)

        # instantiate
        # formułka konfiguracji funkcji odczytu baz danych.
        config = ConfigParser()
        # parse existing file
        config.read('database.ini')
        # read values from a section
        host = config.get('db_setup', 'host')
        port = config.get('db_setup', 'port')
        db_base = config.get('db_setup', 'database')
        user = config.get('db_setup', 'user')
        password = config.get('db_setup', 'password')
        update_val = config.get('db_update', 'date')

        # Updates database if it's the first visit that day.
        fulldate = datetime.date.today()
        currday = str(fulldate.day)
        db = "dbname={0} user={1} password={2}".format(
         db_base, user, password)
        if currday == update_val:
            print('database up to date')
            pass
        else:
            config.set('update', 'date', currday)
            udb = Updatedb()
            udb.connect(user, password, host, port, db_base, db, )
            print('database updated successfully')
            # OszczędnośĆ zasobów. Nie aktualizuje bazy danych,
            # kiedy nikt nie korzysta z aplikacji.

        # Lączenie z bazą danych...
        self.conn = psycopg2.connect(db)
        self.cur = self.conn.cursor()

    # Select piece of database queries by date function
    # Zaznacza wycinek bazy danych ograniczony wyborem użytkownika.
    def selectdate(self, day1, month1, year1, day2, month2, year2, ):
        if self.base == 1 or 4:
            lessq = '='
            moreq = '='
            sign = ['MIN', 'MAX']
        else:
            lessq = '<='
            moreq = ">="
            sign = ['MAX', 'MIN']
        rowfrom = (self.cur.fetchone()[0])
        rowto = (self.cur.fetchone()[0])-rowfrom
        if self.base == 4:
            range = "1"
            execall = '''SELECT "2", "3", "4", "5", "6", "7", "8", "9", "10"
            FROM {0} LIMIT {1} OFFSET {2}'''.format(
             self.table, rowto, rowfrom, )
        else:
            range = "0"
            execall = 'SELECT * FROM {0} LIMIT {1} OFFSET {2}'.format(
             self.table, rowto, rowfrom, )
        selquery = '''SELECT {0}({1}) FROM {2} WHERE "2" {3} {4} AND "3"={5}
         AND "4"={6}'''.format(
         sign[0], range, self.table, lessq, day2, month2, year2, )
        selquery_ = '''SELECT {0}({1}) FROM {2} WHERE "2" {3} {4} AND "3"={5}
         AND "4"={6}'''.format(
         sign[1], range, self.table, moreq, day2, month2, year2, )
        self.cur.execute(selquery)
        self.cur.execute(selquery_)
        self.cur.execute(execall)
        rows = self.cur.fetchall()
        return rows

    def searchall(self, table, ):
        query = 'SELECT * FROM {0}'.format(table)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()


# Ta podfunkcja rekonwertująca bazę danych do df
# aby można było zrobić graf i inne fajne rzeczy na liczbach...
# Zwraca najwyższą, najniższą liczbę, oraz liczby od najczęstszej.
class Dataframe(Database):
    def __init__(self, request, ):
        super().__init__(self, request, )
        if datal is True:
            avg = bool(aver == "1")
            grap = bool(graph == "1")
            query = 'SELECT * FROM %s' (self.table)
            par = ""
        else:
            query = 'SELECT * FROM game1 LIMIT %s OFFSET %s'
            par = "params=[rowto, rowfrom],"
            df = pandas.read_sql_query(
             sql=(query), con=psycopg2.connect(db),
             coerce_float=False, parse_dates=None, chunksize=None)

        if base == 4:
            df1 = df.drop(df.columns[0:4], 1)
            df1 = df1.drop(df.columns[-1], 1)
        else:
            df1 = df.drop(df.columns[0:num], 1)

    def extremes(self, num=5):
        if base != 4:
            df1(num)
        df2 = df1.apply(pandas.value_counts).fillna(0)
        df2.loc[:, 'total'] = df2.sum(axis=1)
        df3 = df2

        nplus = df3.sort_values(
         ['total'], ascending=[False])[:1].index.values
        nminus = df3.sort_values(
         ['total'], ascending=[False])[-1:].index.values
        nums = df3.sort_values(
         ['total'], ascending=[False])[:int(value)].index.values

        if var1 == '1':
            hilow = "Max: " + str(nplus) + "  Min: " + str(nminus)
        else:
            hilow = "Nie wybrano liczb skrajnych"
        if int(value) > 0:
            often = "Od najczęstszej: " + str(nums)
        else:
            "Nie wybrano najczęstszych liczb"

    def makedf(self, base, avg, grap, num=3):
        global sourcef
        global avgsc
        if base != 4:
            df1(num)
        df4 = df1.T
        df5 = df4.mean().round(0).value_counts()
        slist = list()
        nrlist = list()
        while len(slist) < len(df5.index):
            slist.append(" / ")
        while len(nrlist) < len(df5.index):
            nrlist.append("\n")
        dfindex = df5.index.astype(str)
        dfvalue = df5.values.astype(str)
        zipped = zip(dfindex, slist, dfvalue, nrlist)
        a = list(zipped)
        ahead = ["Średnia" + " / " + "Częstotliwość" + "\n" ]
        b = ahead + a

        source = ColumnDataSource(
            data=dict(
                Means=df5.index,
                Freqs=df5.values
                ))
        if avg is True:
            avgsc = b
        else:
            avgsc = "Nie wybrano generowania średnich"
        if grap is True:
            # makegraph() tutaj muszę popracowaĆ nad integracją bokeh z django
            pass


# Główna oś funkcji
def generate(request):
    global datal
    global nhilo
    global norol
    global moftn
    global avsco
    global grgen
    global datfro
    global dattoo
    if request.is_ajax():
        radio = request.POST.get('gamesel')
        datfr = re.findall(
                 r"(\d\d\d\d)-(\d\d)-(\d\d)", request.POST['datefrom'])
        datto = re.findall(
                 r"(\d\d\d\d)-(\d\d)-(\d\d)", request.POST['dateto'])
        datal = request.POST['dateall']
        nhilo = request.POST['numhilow']
        norol = request.POST['norolls']
        moftn = request.POST['mostoften']
        avsco = request.POST['avgscores']
        grgen = request.POST['graphgen']

    if datal == "0":
        datfro = datfr[0]
        dattoo = datto[0]
        database.selectdate(
                            base, table, dattoo[2], dattoo[1], dattoo[0],
                            datfro[2], datfro[1], datfro[0], )
        datal = False
    elif datal == "1":
        database.searchall(table)
        datal == True
    else:
        bug_catch()

    dataframes.extremes(radio,moftn,nhilo)
    dataframes.makedf(radio,avsco,grgen)

    if norol == '1':
        rolls = "Nie wybrano losowań"
    elif norol == "0" and datal == "0":
        rollhead = ["Losowania wraz z datą:" + "\n"]
        rowspacing = list()
        while len(rowspacing)<len(rows):
            rowspacing.append("\n")
        zippedrows = zip(rows, rowspacing)
        ziprows = list(zippedrows)
        rolls = [rollhead, ziprows]
    elif norol == "0" and datal == "1":
        rolls = "Zaznaczono całość pomiarów"
    else:
        bug_catch()

    responsedata = {
        'hilow' : hilow,
        'rolls' : rolls,
        'often' : often,
        'avgsc' : avgsc,
#Co do ostatniego to możliwe, że trzeba będzie dodaĆ warunkowe return/render HttpResponse pod ten graf.
        'graph' : graph
    }
    return JsonResponse(responsedata)
# Zwraca najwyższą, najniższą liczbę, oraz liczby od najczęstszej.


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