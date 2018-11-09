import pandas
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource


    (type(radio)
    (type(datfr)
    (type(datto)
    (type(datal)
    (type(nhilo)
    (type(norol)
    (type(moftn)
    (type(avsco)
    (type(grgen)
#Można uży tej funkcji do uporządkowania spraw z backendem tak żeby go nie przepisywa w całości.
#To fukcja przypisująca numery od 1 do 8 w zależności od przypadku pazy danych i tego czy
# jest filtrowana czy nie.
def radparam():
    global rad
    if datal + radio == "11" :
        rad = 1
    elif datal + radio == "12" :
        rad = 2
    elif datal + radio == "13" :
        rad = 3
    elif datal + radio == "14" :
        rad = 4
    elif datal + radio == "01" :
        randback.searchA(1,dt2.day,dt2.month,dt2.year,dt1.day,dt1.month,dt1.year)
        rad = 5
    elif datal + radio == "02" :
        randback.searchA(2,dt2.day,dt2.month,dt2.year,dt1.day,dt1.month,dt1.year)
        rad = 6
    elif datal + radio == "03" :
        randback.searchA(3,dt2.day,dt2.month,dt2.year,dt1.day,dt1.month,dt1.year)
        rad = 7
    elif datal + radio == "04" :
        randback.searchA(4,dt2.day,dt2.month,dt2.year,dt1.day,dt1.month,dt1.year)
        rad = 8
    else:
        pass

#Ta funkcja ogranicza bazę rakordów do konkretnych dat.
def searchA(base,day1,month1,year1,day2,month2,year2):
    conn=sqlite3.connect("Lotto.db")
    cur=conn.cursor()
    global rowfrom
    global rowto
    if base == 1:
        cur.execute('SELECT MIN(rowid) FROM game1 WHERE "2"=? AND "3"=? AND "4"=?',(day2,month2,year2))
        rowfrom=(cur.fetchone()[0])
        cur.execute('SELECT MAX(rowid) FROM game1 WHERE "2"=? AND "3"=? AND "4"=?',(day1,month1,year1))
        rowto=(cur.fetchone()[0])-rowfrom
        cur.execute('SELECT * FROM game1 LIMIT ? OFFSET ?', (rowto, rowfrom))
    elif base == 2:
        cur.execute('SELECT MAX(rowid) FROM game2 WHERE "2"<=? AND "3"=? AND "4"=?',(day2,month2,year2))
        rowfrom=(cur.fetchone()[0])
        cur.execute('SELECT MIN(rowid) FROM game2 WHERE "2">=? AND "3"=? AND "4"=?',(day1,month1,year1))
        rowto=(cur.fetchone()[0])-rowfrom
        cur.execute('SELECT * FROM game2 LIMIT ? OFFSET ?', (rowto, rowfrom))
    elif base == 3:
        cur.execute('SELECT MAX(rowid) FROM game3 WHERE "2"<=? AND "3"=? AND "4"=?',(day2,month2,year2))
        rowfrom=(cur.fetchone()[0])
        cur.execute('SELECT MIN(rowid) FROM game3 WHERE "2">=? AND "3"=? AND "4"=?',(day1,month1,year1))
        rowto=(cur.fetchone()[0])-rowfrom
        cur.execute('SELECT * FROM game3 LIMIT ? OFFSET ?', (rowto, rowfrom))
    elif base == 4:
        cur.execute('SELECT MIN("1") FROM game4 WHERE "2"=? AND "3"=? AND "4"=?',(day2,month2,year2))
        rowfrom=(cur.fetchone()[0])
        cur.execute('SELECT MAX("1") FROM game4 WHERE "2"=? AND "3"=? AND "4"=?',(day1,month1,year1))
        rowto=(cur.fetchone()[0])-rowfrom
        cur.execute('SELECT "2", "3", "4", "5", "6", "7", "8", "9", "10" FROM game4 LIMIT ? OFFSET ?', (rowto, rowfrom))
    rows=cur.fetchall()
    conn.close()
#    return rows

#Funkcja searchall dla checkboxa ściągająca dane z całej bazy danych. .
def searchallbox(var):
    conn=sqlite3.connect("Lotto.db")
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
            con=sqlite3.connect("Lotto.db"), coerce_float=False, parse_dates=None, chunksize=None)
    elif var == 2 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game2'),
            con=sqlite3.connect("Lotto.db"), coerce_float=False, parse_dates=None, chunksize=None)
    elif var == 3 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game3'),
            con=sqlite3.connect("Lotto.db"), coerce_float=False, parse_dates=None, chunksize=None)
    elif var == 4 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game4'),
            con=sqlite3.connect("Lotto.db"), coerce_float=False, parse_dates=None, chunksize=None)
    elif var == 5 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game1 LIMIT ? OFFSET ?'),
            con=sqlite3.connect("Lotto.db"), coerce_float=False, params=[rowto, rowfrom], parse_dates=None, chunksize=None)
    elif var == 6 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game2 LIMIT ? OFFSET ?'),
            con=sqlite3.connect("Lotto.db"), coerce_float=False, params=[rowto, rowfrom], parse_dates=None, chunksize=None)
    elif var == 7 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game3 LIMIT ? OFFSET ?'),
            con=sqlite3.connect("Lotto.db"), coerce_float=False, params=[rowto, rowfrom], parse_dates=None, chunksize=None)
    elif var == 8 :
        df = pandas.read_sql_query(
            sql=('SELECT * FROM game4 LIMIT ? OFFSET ?'),
            con=sqlite3.connect("Lotto.db"), coerce_float=False, params=[rowto, rowfrom], parse_dates=None, chunksize=None)

#Zwraca najwyższą, najniższą liczbę, oraz liczby od najczęstszej.
def enumerators(base,value,var1):
    dfdb(base)
    if base == 4 or base == 8 :
        df1=df.drop(df.columns[0:4],1)
        df1=df1.drop(df.columns[-1],1)
    else:
        df1=df.drop(df.columns[0:3],1)
    df2 = df1.apply(pandas.value_counts).fillna(0);
    df2.loc[:,'total'] = df2.sum(axis=1)
    df3=df2
    nplus = df3.sort_values(['total'], ascending=[False])[:1].index.values;
    nminus = df3.sort_values(['total'], ascending=[False])[-1:].index.values;
    nums = df3.sort_values(['total'], ascending=[False])[:int(value)].index.values;
    if int(value) > 0 :
        var2 == 1
    else:
        var2 == 0
    if var1 == '1' and var2 == '1' :
        yield "Max: " + str(nplus) + "  Min: " + str(nminus)
        yield "Od najczęstszej: " + str(nums)
    elif var1 == '1' and var2 == '0' :
        yield "Max: " + str(nplus) + "  Min: " + str(nminus)
    elif var1 == '0' and var2 == '1' :
        yield "Od najczęstszej: " + str(nums)

#Nadfunkcja - Zwraca graf i średnie wyników losowań.
def makedf(base,var1,var2):
    dfdb(base)
    global df1
    if base == 4 or base == 8 :
        df1=df.drop(df.columns[0:4],1)
        df1=df1.drop(df.columns[-1],1)
    else:
        df1=df.drop(df.columns[0:3],1)
    df4=df1.T
    df5=df4.mean().round(0).value_counts()
    slist = list()
    while len(slist)<len(df5.index):
        slist.append(" / ")
    zipped = zip(df5.index, slist, df5.values)
    a=list(zipped)
    global source
    source = ColumnDataSource(
        data=dict(
            Means=df5.index,
            Freqs=df5.values
            ))
    if var1 == '1' and var2 == '1':
            makegraph()
            return a
    elif var1 == '0' and var2 == '1':
            makegraph()
    elif var1 == '1' and var2 == '0':
            return a

#Ta funkcja wyciąga z bazy danych pierwszą/ostatnią datę. (W wersji webowej do zaimplementowania na końcu...)
def getcaldate(base, date):
    conn=sqlite3.connect("Lotto.db")
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
    return rows
