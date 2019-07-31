import psycopg2
import pandas
import urllib.request
from bs4 import BeautifulSoup
import re
import ssl
from sqlalchemy import create_engine
import configparser
import datetime
import os


def gotolast(ctx):
    url = 'https://www.wynikilotto.net.pl/ekstra-pensja/wyniki/'
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    a = str(soup.find_all('td'))
    p = re.findall(r">(\d\d\d\d)<", a)
    return(p[-1])


class Updatedb(object):
    ''' Klasa aktualizująca bazę danych randomizera,
    współpracuje z database.ini przy pomocy configparsera.'''

    def __init__(self):
        # instantiate
        # formułka konfiguracji funkcji odczytu baz danych.
        config = configparser.ConfigParser()
        # parse existing file
        config.read('database.ini')
        # read values from a section
        self.host = config.get('db_setup', 'host')
        self.port = config.get('db_setup', 'port')
        self.db_base = config.get('db_setup', 'db_base')
        self.user = config.get('db_setup', 'user')
        self.password = config.get('db_setup', 'password')
        update_val = config.get('db_update', 'date')

        # Updates database if it's the first visit that day.
        fulldate = datetime.date.today()
        currday = str(fulldate)
        print('today is ' + currday)
        if currday == update_val:
            print('database up to date')
            pass
        else:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            # Funkcja znajduje zawsze ostatnią stronę wyników.
            rl = 'https://www.wynikilotto.net.pl/ekstra-pensja/wyniki/'
            url = rl + str(gotolast(ctx))
            html = urllib.request.urlopen(url, context=ctx).read()
            soup = BeautifulSoup(html, 'html.parser')
            lsource = str(soup.find_all('td'))
            g1 = re.findall(
             r">(\d\d\d\d)</td>, <td>(\d\d)[.](\d\d)[.](\d\d\d\d)</td>," +
             " <td>(\d\d) (\d\d) (\d\d) (\d\d) (\d\d) [+] <b>(\d\d)<",
             lsource)
            print(g1)

            x = 1
            gra = (' ', 'http://www.mbnet.com.pl/ml.txt',
                   'http://www.mbnet.com.pl/dl.txt',
                   'http://www.mbnet.com.pl/el.txt')
            db_ini = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
             self.user, self.password, self.host, self.port, self.db_base, )
            engine = create_engine(db_ini)
            print('Updating databases...')
            while x < 4:
                print(gra[x])
                table = 'game' + str(x)
                df = pandas.read_csv(gra[x], header=None, sep='[., ]',
                                     engine='python')
                df.to_sql(table, engine, if_exists="replace", index=False)
                print('updated db ' + str(x) + '...')
                x = x + 1
                conn = engine.raw_connection()
                cur = conn.cursor()
                conn.commit()
                conn.close()
            print('updated dfs')

            conn = psycopg2.connect(
             dbname=self.db_base, user=self.user,
             host=self.host, password=self.password,)
            print('connected to db4')
            cur = conn.cursor()
            cur.execute(
             '''CREATE TABLE IF NOT EXISTS game4 ("1" INTEGER UNIQUE,
             "2" INTEGER, "3" INTEGER, "4" INTEGER, "5" INTEGER, "6" INTEGER,
             "7" INTEGER, "8" INTEGER, "9" INTEGER, "10" text)''')
            cur.execute(
             '''CREATE UNIQUE INDEX IF NOT EXISTS idx_casenum
             ON game4 ("1")''')
            cur.executemany(
             '''INSERT INTO game4 ("1","2","3","4","5","6","7","8","9","10")
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ("1")
             Do NOTHING''', [(v) for v in g1])
            print('updated db 4...')
            conn.commit()
            conn.close()
            print('connection closed')
            config.set('db_update', 'date', currday)
            with open("database.ini.new", "w") as fh:
                config.write(fh)
            os.rename("database.ini", "database.ini~")
            os.rename("database.ini.new", "database.ini")
            print('current date set to:' + currday)
            print('database updated successfully')
