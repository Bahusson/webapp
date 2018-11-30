import psycopg2
import pandas
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import ssl
from sqlalchemy import create_engine
import configparser
from lotto import randomize

        #Zaprogramuj tę funkcję na serwerze tak, aby raz dziennie o północy odnawiała bazę danych.
        #Opcjonalnie dla oszczędzania zasobów możesz zrobi tak, żeby za pierwszym razem danego dnia
        #jak ktoś zrobi to zapytanie i tylko ten raz baza się odnawiała. Masz podobną funkcję przy
        #guziku zapisu.

        #Ten kawałek to parser beautifulsoup i regular expressions dla ekstra pensji, bo na mbtnet nie ma bazy w CSV.
class Updatedb(self):
    database():
    def __init__(self):
        url = 'https://www.wynikilotto.net.pl/ekstra-pensja/wyniki/'
        html = urllib.request.urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        a = str(soup.find_all('td'))
        p = re.findall(">(\d\d\d\d)<", a)
        url = 'https://www.wynikilotto.net.pl/ekstra-pensja/wyniki/'+str(p)
        lsource = str(soup.find_all('td'))
        g1 = re.findall(">(\d\d\d\d)</td>, <td>(\d\d)[.](\d\d)[.](\d\d\d\d)</td>, <td>(\d\d) (\d\d) (\d\d) (\d\d) (\d\d) [+] <b>(\d\d)<", lsource)

        ctx = ssl.create_default_context()
        ctx.check_hostname = False

    def connect():
        x=5
        query=
        while x > 0:
            x=x-1
            gra = {multi : 'http://www.mbnet.com.pl/ml.txt',
                   lotek : 'http://www.mbnet.com.pl/dl.txt',
                   mini  : 'http://www.mbnet.com.pl/el.txt'}
            db_ini = 'postgresql+psycopg2://postgres:Ma3taksamo_Jakja@localhost:5432/webappbasedb'
            engine = create_engine(db_ini
            if var == 1:
                query = table + ', engine,if_exists="replace",index=False']
                df = pandas.read_csv('http://www.mbnet.com.pl/ml.txt',header =None, sep='[., ]', engine ='python')
                df.to_sql(query[] #truncates the table


            elif var == 2 :
                df = pandas.read_csv('http://www.mbnet.com.pl/dl.txt',header =None, sep='[., ]', engine ='python')
            elif var == 3 :
                df = pandas.read_csv('http://www.mbnet.com.pl/el.txt',header =None, sep='[., ]', engine ='python')
            conn = engine.raw_connection()
            cur = conn.cursor()
            conn.commit()

        elif var == 4 :
            conn=psycopg2.connect("dbname=webappbasedb user=postgres password=Ma3taksamo_Jakja")
            cur=conn.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS game4 ("1" INTEGER UNIQUE, "2" INTEGER, "3" INTEGER, "4" INTEGER, "5" INTEGER, "6" INTEGER, "7" INTEGER, "8" INTEGER, "9" INTEGER, "10" text)')
            cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_casenum ON game4 ("1")')
            cur.executemany('INSERT INTO game4 ("1","2","3","4","5","6","7","8","9","10") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ("1") DO NOTHING', [(v) for v in g1])
        conn.commit()
        conn.close()

    def connectall():
        connect(1)
        connect(2)
        connect(3)
        connect(4)
