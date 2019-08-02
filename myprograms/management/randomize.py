# from django.http import JsonResponse, HttpResponse
import psycopg2
import pandas
# from bokeh.plotting import figure, output_file, show
# from bokeh.models import HoverTool, ColumnDataSource
import random
import re
from .commands.updatedb import Updatedb


# Żeby uniknąć zdań warunkowych wykorzystaj polimorfizm dla bazy 4!
class Database(object):
    '''Klasa rodzic - wzywa bazę danych do aktualizacji przy każdym
    uruchomieniu (o ile nie była już aktualizowana danego dnia),
    oraz kalkuluje całość lub fragment pomiarów. '''

    def __init__(self, request):
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

        # Zaktualizuj bazę danych.
        udb = Updatedb()
        # Lączenie z bazą danych...
        self.conn = psycopg2.connect(
         dbname=udb.db_base, user=udb.user,
         host=udb.host, password=udb.password, )
        self.cur = self.conn.cursor()

    # Select piece of database queries by date function
    # Zaznacza wycinek bazy danych ograniczony wyborem użytkownika.
    def selectdate(self):
        date_from = self.datfr[0]
        date_to = self.datto[0]
        range = "0"
        lessq = '<='
        moreq = '>='
        sign = ['MAX', 'MIN']
        if self.base == 1 or 4:
            lessq = '>='
            moreq = '<='
            sign = ['MIN', 'MAX']
            if self.base == 4:
                range = "1"

        selquery = '''SELECT {0}("{1}") FROM {2} WHERE "2" {3} {4}
         AND "3" = {5} AND "4" = {6}'''.format(
          sign[0], range, self.table, lessq,
          date_from[2], date_from[1], date_from[0], )
        selquery_ = '''SELECT {0}("{1}") FROM {2} WHERE "2" {3} {4}
         AND "3" = {5} AND "4" = {6}'''.format(
          sign[1], range, self.table, moreq,
          date_to[2], date_to[1], date_to[0], )
        self.cur.execute(selquery)
        self.rowfrom = self.cur.fetchone()[0]
        self.cur.execute(selquery_)
        self.rowto = self.cur.fetchone()[0] - self.rowfrom
        if self.base == 4:
            self.execall = '''SELECT "2", "3", "4", "5", "6", "7", "8", "9",
             "10" FROM {0} LIMIT {1} OFFSET {2}'''.format(
              self.table, self.rowto, self.rowfrom, )
        else:
            self.execall = '''SELECT * FROM {0} LIMIT {1} OFFSET {2}'''.format(
             self.table, self.rowto, self.rowfrom, )

    def selectall(self):
        self.searchquery = '''SELECT * FROM {0}'''.format(self.table)

    def __del__(self):
        self.conn.close()


class Dataframe(Database):
    ''' Klasa dziecko - Generuje największą i najmniejszą liczbę,
    najczęstsze liczby, średnie, graf, oraz gołe wyniki'''

    def __init__(self, request):
        super().__init__(request)
        if self.all_data == 1:
            super().selectall()
            query = self.searchquery
        else:
            super().selectdate()
            query = self.execall

        self.df = pandas.read_sql_query(
         sql=(query), con=self.conn,
         coerce_float=False, parse_dates=None, chunksize=None)

        if self.base == 4:
            self.df1 = self.df.drop(self.df.columns[0:4], 1)
            self.df1 = self.df1.drop(self.df.columns[-1], 1)

    # Zwraca gołe wyniki z całego okresu pomiarów
    def searchall(self):
        super().selectall()
        self.cur.execute(self.searchquery)
        rows = self.cur.fetchall()
        return rows

    # Zwraca ograniczone wyniki z danego okresu.
    def returndate(self):
        super().selectdate()
        self.cur.execute(self.execall)
        rows = self.cur.fetchall()
        return rows

    # Nadfunkcja - kalkuluje df dla dwóch podfunkcji poniżej.
    def preparedf(self):
        if self.base != 4:
            self.df1 = self.df.drop(self.df.columns[0:5], 1)
        df2 = self.df1.apply(pandas.value_counts).fillna(0)
        df2.loc[:, 'total'] = df2.sum(axis=1)
        df3 = df2
        self.nplus = df3.sort_values(
         ['total'], ascending=[False])[:1].index.values
        self.nminus = df3.sort_values(
         ['total'], ascending=[False])[-1:].index.values
        self.nums = df3.sort_values(
         ['total'], ascending=[False])[:self.mode].index.values

    # Zwraca najwyższą i najniższą liczbę.
    def extremes(self):
        if self.extreme_nums is 1:
            self.preparedf()
            extr = "Max: " + str(self.nplus) + "  Min: " + str(self.nminus)
            return extr
        else:
            return "Nie wybrano liczb skrajnych"

    # Zwraca najczęściej występujące liczby w ilości X od najwyższej.
    def modals(self):
        if int(self.mode) > 0:
            self.preparedf()
            modals = "Od najczęstszej: " + str(self.nums)
            return modals
        else:
            return "Nie wybrano najczęstszych liczb"

    # Nadfunkcja - szykująca df dla dwóch podfunkci poniżej. NIEUKOŃCZONA!
    # W tej chwili po prostu zwraca średnie.
    def makedf(self):
        if self.base != 4:
            self.df1 = self.df.drop(self.df.columns[0:3], 1)
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
        average = ahead + a
    #    source = ColumnDataSource(
    #        data=dict(
    #            Means=df5.index,
    #            Freqs=df5.values
    #            ))
        if self.av_score == 1:
            return average
        else:
            average = "Nie wybrano generowania średnich"
            return average
        if self.gen_graph == 1:
            # makegraph() tutaj muszę popracowaĆ nad integracją bokeh z django
            pass

    def __del__(self):
        super().__del__()
    # def __del__(self):
    #     self.conn.close()


def randomroll(request):
    # Ta funkcja generuje losowe wyniki dla wybranej gry.
    radio = request.POST['gamesel']
    rangedict = {"1": 80, "2": 50, "3": 43, "4": 36, }
    kdict = {"1": 20, "2": 6, "3": 5, "4": 5, }
    lst1 = []
    lst1.append(sorted(random.sample(
     list(range(1, rangedict[radio])), kdict[radio])))
    if radio == "4":
        lst1.append(random.sample(list(range(1, 5)), k=1))
    return lst1
