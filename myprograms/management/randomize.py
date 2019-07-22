from django.http import JsonResponse, HttpResponse
import psycopg2
import pandas
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource
import re
import ConfigParser
import datetime
from .managment.commands.updatedb import Updatedb


# Żeby uniknąć zdań warunkowych wykorzystaj polimorfizm dla bazy 4!
class Database(object):

    def __init__(self, request):
        if request.is_ajax():  # Czy można bez If request is ajax?
            # Albo wyrzucić request is ajax do views?
            def intistrue(x):
                bool(int(x == 1))

            self.base = int(request.POST.get('gamesel'))
            self.datfr = re.findall(r"(\d\d\d\d)-(\d\d)-(\d\d)",
                                    request.POST['datefrom'])
            self.datto = re.findall(r"(\d\d\d\d)-(\d\d)-(\d\d)",
                                    request.POST['dateto'])
            self.datal = intistrue(request.POST['dateall'])
            self.nhilo = intistrue(request.POST['numhilow'])
            self.norol = intistrue(request.POST['norolls'])
            self.moftn = int(request.POST['mostoften'])
            self.avsco = intistrue(request.POST['avgscores'])
            self.grgen = intistrue(request.POST['graphgen'])
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
        self.db = "dbname={0} user={1} password={2}".format(
         db_base, user, password)
        if currday == update_val:
            print('database up to date')
            pass
        else:
            config.set('update', 'date', currday)
            udb = Updatedb()
            udb.connect(user, password, host, port, db_base, self.db, )
            print('database updated successfully')
            # OszczędnośĆ zasobów. Nie aktualizuje bazy danych,
            # kiedy nikt nie korzysta z aplikacji.

        # Lączenie z bazą danych...
        self.conn = psycopg2.connect(self.db)
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
    def __init__(self, request, num=3):
        super().__init__(self, request, )
        if self.datal is True:
            query = 'SELECT * FROM %s' (self.table)
            par = ""
        else:
            query = 'SELECT * FROM game1 LIMIT %s OFFSET %s'
            par = "[rowto, rowfrom],"
            df = pandas.read_sql_query(
             sql=(query), con=psycopg2.connect(self.db),
             coerce_float=False, parse_dates=None, params=par, chunksize=None)

        if self.base == 4:
            df1 = df.drop(df.columns[0:4], 1)
            self.df1 = df1.drop(df.columns[-1], 1)
        else:
            self.df1 = df.drop(df.columns[0:num], 1)

    def extremes(self, value, var1, num=5):
        if self.base != 4:
            self.df1(num)
        df2 = self.df1.apply(pandas.value_counts).fillna(0)
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
        yield hilow

        if int(value) > 0:
            often = "Od najczęstszej: " + str(nums)
        else:
            "Nie wybrano najczęstszych liczb"
        yield often

    def makedf(self, num=3):
        global sourcef
        global avgsc
        if self.base != 4:
            self.df1(num)
        df4 = self.df1.T
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
        ahead = ["Średnia" + " / " + "Częstotliwość" + "\n"]
        b = ahead + a

        source = ColumnDataSource(
            data=dict(
                Means=df5.index,
                Freqs=df5.values
                ))
        if self.avsco is True:
            avgsc = b
        else:
            self.avgsc = "Nie wybrano generowania średnich"
        yield avgsc

        if self.grgen is True:
            # makegraph() tutaj muszę popracowaĆ nad integracją bokeh z django
            pass
