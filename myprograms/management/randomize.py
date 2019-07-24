# from django.http import JsonResponse, HttpResponse
import psycopg2
import pandas
# from bokeh.plotting import figure, output_file, show
# from bokeh.models import HoverTool, ColumnDataSource
import re
import configparser
import datetime
from .commands.updatedb import Updatedb


# Żeby uniknąć zdań warunkowych wykorzystaj polimorfizm dla bazy 4!
class Database(object):
    '''Klasa rodzic, wzywa bazę danych do aktualizacji przy każdym uruchomieniu
    o ile nie była już aktualizowana danego dnia,
    oraz zwraca całość lub fragment pomiarów. '''

    def __init__(self, request):
        if request.is_ajax():  # Czy można bez If request is ajax?
            # Albo wyrzucić request is ajax do views?

            self.base = int(request.POST.get('gamesel'))
            self.all_data = int(request.POST['dateall'])
            self.datfr = re.findall(r"(\d\d\d\d)-(\d\d)-(\d\d)",
                                    request.POST['datefrom'])
            self.datto = re.findall(r"(\d\d\d\d)-(\d\d)-(\d\d)",
                                    request.POST['dateto'])
            self.extreme_nums = int(request.POST['numhilow'])
            self.no_rolls = int(request.POST['norolls'])
            self.mode = int(request.POST['mostoften'])
            self.av_score = int(request.POST['avgscores'])
            self.gen_graph = int(request.POST['graphgen'])
            self.table = "game" + str(self.base)

        # instantiate
        # formułka konfiguracji funkcji odczytu baz danych.
        config = configparser.ConfigParser()
        # parse existing file
        config.read('database.ini')
        # read values from a section
        host = config.get('db_setup', 'host')
        print(host)
        port = config.get('db_setup', 'port')
        db_base = config.get('db_setup', 'db_base')
        user = config.get('db_setup', 'user')
        password = config.get('db_setup', 'password')
        update_val = config.get('db_update', 'date')

        # Updates database if it's the first visit that day.
        fulldate = datetime.date.today()
        currday = str(fulldate.day)
        print('today is ' + currday)
        # self.db = "database={0} user={1} host={2} password={3}".format(
        # db_base, user, host, password)
        if currday == update_val:
            print('database up to date')
            pass
        else:
            udb = Updatedb(user, password, host, port, db_base, )
            udb
            print('database updated successfully')
            config.set('db_update', 'date', currday)
            print('current date set to:' + currday)
            # OszczędnośĆ zasobów. Nie aktualizuje bazy danych,
            # kiedy nikt nie korzysta z aplikacji.

        # Lączenie z bazą danych...
        self.conn = psycopg2.connect(
         dbname=db_base, user=user, host=host, password=password, )
        self.cur = self.conn.cursor()
        # self.rowfrom = self.cur.fetchone()[0]
        # self.rowto = self.cur.fetchone()[0]-self.rowfrom

    # Select piece of database queries by date function
    # Zaznacza wycinek bazy danych ograniczony wyborem użytkownika.
    def selectdate(self):
        date_from = self.datfr[0]
        date_to = self.datto[0]
        self.rowto = ''  # Empty string bo go muszę zadeklarować przed użyciem
        self.rowfrom = ''  # inaczej się robi bałagan. Nie mam lepszego pomysłu
        if self.base == 1 or 4:
            lessq = '='
            moreq = '='
            sign = ['MIN', 'MAX']
        else:
            lessq = '<='
            moreq = ">="
            sign = ['MAX', 'MIN']
        if self.base == 4:
            range = "1"
            execall = '''SELECT "2", "3", "4", "5", "6", "7", "8", "9", "10"
            FROM {0} LIMIT {1} OFFSET {2}'''.format(
             self.table, self.rowto, self.rowfrom, )
        else:
            range = "0"
            execall = '''SELECT * FROM {0} LIMIT {1} OFFSET {2}'''.format(
             self.table, self.rowto, self.rowfrom, )
        selquery = '''SELECT {0}({1}) FROM {2} WHERE "2" {3} {4} AND "3" = {5}
         AND "4" = {6}'''.format(
         sign[0], range, self.table, lessq,
         date_from[2], date_from[1], date_from[0], )
        selquery_ = '''SELECT {0}({1}) FROM {2} WHERE "2" {3} {4} AND "3" = {5}
         AND "4" = {6}'''.format(
         sign[1], range, self.table, moreq,
         date_to[2], date_to[1], date_to[0], )
        self.cur.execute(selquery)
        self.rowfrom = self.cur.fetchone()[0]
        print(self.rowfrom)
        self.cur.execute(selquery_)
        self.rowto = self.cur.fetchone()[0] - self.rowfrom
        print(self.rowto)
        self.cur.execute(execall)
        rows = self.cur.fetchall()
        return rows

    def searchall(self):
        query = '''SELECT * FROM {0}'''.format(self.table)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()


class Dataframe(Database):
    ''' Generuje największą i najmniejszą liczbę,
    najczęstsze liczby, średnie i graf'''

    def __init__(self, request, num=3):
        super().__init__(request)
        if self.all_data == 1:
            query = '''SELECT * FROM {0}'''.format(self.table)
            # par = ""
        else:
            super().selectdate()
            query = '''SELECT * FROM {0} LIMIT {1} OFFSET {2}'''.format(
                    self.table, self.rowto, self.rowfrom)
            # par = "[self.rowto, self.rowfrom],"
        df = pandas.read_sql_query(
         sql=(query), con=self.conn,
         coerce_float=False, parse_dates=None, chunksize=None)

        if self.base == 4:
            df1 = df.drop(df.columns[0:4], 1)
            self.df1 = df1.drop(df.columns[-1], 1)
        else:
            self.df1 = df.drop(df.columns[0:num], 1)

    def extremes(self, num=5):
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
         ['total'], ascending=[False])[:self.mode].index.values

        if self.extreme_nums is True:
            self.extr = "Max: " + str(nplus) + "  Min: " + str(nminus)
        else:
            self.extr = "Nie wybrano liczb skrajnych"

        if int(self.mode) > 0:
            self.modals = "Od najczęstszej: " + str(nums)
        else:
            self.modals = "Nie wybrano najczęstszych liczb"

    def makedf(self, num=3):
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

    #    source = ColumnDataSource(
    #        data=dict(
    #            Means=df5.index,
    #            Freqs=df5.values
    #            ))
        if self.av_score == 1:
            self.average = b
        else:
            self.average = "Nie wybrano generowania średnich"

        if self.gen_graph == 1:
            # makegraph() tutaj muszę popracowaĆ nad integracją bokeh z django
            pass

    def __del__(self):
        self.conn.close()
        # super().__del__()
