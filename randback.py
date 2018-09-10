import sqlite3
import pandas
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import ssl

#Ten kawałek to parser beautifulsoup i regular expressions dla ekstra pensji, bo na mbtnet nie ma bazy w CSV.
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def gotolast():
    url = 'https://www.wynikilotto.net.pl/ekstra-pensja/wyniki/'
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    a = str(soup.find_all('td'))
    p = re.findall(">(\d\d\d\d)<", a)
    return(p[-1])

url = 'https://www.wynikilotto.net.pl/ekstra-pensja/wyniki/'+str(gotolast())
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')
lsource = str(soup.find_all('td'))
g1 = re.findall(">(\d\d\d\d)</td>, <td>(\d\d)[.](\d\d)[.](\d\d\d\d)</td>, <td>(\d\d) (\d\d) (\d\d) (\d\d) (\d\d) [+] <b>(\d\d)<", lsource)

#Na starcie łączy się z siecią i aktualizuje bazy danych dla wszystkich 4 gier losowych.
def connect(var):
    conn=sqlite3.connect("Lotto.db")
    cur=conn.cursor()
    if var == 1 :
        df = pandas.read_csv('http://www.mbnet.com.pl/ml.txt',header =None, sep='[., ]', engine ='python')
        df1= df.drop(df.columns[0:2],1)
        df1.to_sql('game1', conn, if_exists='replace', index=False)
    elif var == 2 :
        df = pandas.read_csv('http://www.mbnet.com.pl/dl.txt',header =None, sep='[., ]', engine ='python')
        df1= df.drop(df.columns[0:2],1)
        df1.to_sql('game2', conn, if_exists='replace', index=False)
    elif var == 3 :
        df = pandas.read_csv('http://www.mbnet.com.pl/el.txt',header =None, sep='[., ]', engine ='python')
        df1= df.drop(df.columns[0:2],1)
        df1.to_sql('game3', conn, if_exists='replace', index=False)
    elif var == 4 :
        cur.execute('CREATE TABLE IF NOT EXISTS game4 ("1" INTEGER, "2" INTEGER, "3" INTEGER, "4" INTEGER, "5" INTEGER, "6" INTEGER, "7" INTEGER, "8" INTEGER, "9" INTEGER, "10" INTEGER)')
        cur.executemany('INSERT OR REPLACE INTO game4 ("1","2","3","4","5","6","7","8","9","10") VALUES (?,?,?,?,?,?,?,?,?,?)', g1)
        cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_casenum ON game4 ("1")')
    conn.commit()
    conn.close()


#funkcja szukająca po dacie
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
    return rows

#Funkcja searchall dla checkboxa ściągająca dane z całej bazy danych. .
def searchallbox(var):
    conn=sqlite3.connect("Lotto.db")
    cur=conn.cursor()
    if var == 1 :
        cur.execute('SELECT * FROM game1')
    elif var == 2 :
        cur.execute('SELECT * FROM game2')
    elif var == 3 :
        cur.execute('SELECT * FROM game3')
    elif var == 4 :
        cur.execute('SELECT "2", "3", "4", "5", "6", "7", "8", "9", "10" FROM game4')
    rows=cur.fetchall()
    conn.close()
    return rows

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

#To funkcja rekonwertująca bazę danych do df aby można było zrobić graf i inne fajne rzeczy na liczbach...

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

def enumerators(base,value,var1,var2):
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
    if var1 == 1 and var2 == 1 :
        yield "Max: " + str(nplus) + "  Min: " + str(nminus)
        yield "Od najczęstszej: " + str(nums)
    elif var1 == 1 and var2 == 0 :
        yield "Max: " + str(nplus) + "  Min: " + str(nminus)
    elif var1 == 0 and var2 == 1 :
        yield "Od najczęstszej: " + str(nums)

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
    if var1 == 1 and var2 == 1:
            makegraph()
            return a
    elif var1 == 0 and var2 == 1:
            makegraph()
    elif var1 == 1 and var2 == 0:
            return a

#Ta funkcja wyciąga z bazy danych pierwszą/ostatnią datę.
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

connect(1)
connect(2)
connect(3)
connect(4)
