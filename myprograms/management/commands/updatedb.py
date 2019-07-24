import psycopg2
import pandas
import urllib.request
from bs4 import BeautifulSoup
import re
import ssl
from sqlalchemy import create_engine


class Updatedb(object):
    ''' Klasa aktualizująca bazę danych randomizera '''

    def __init__(self, user, password, host, port, db_base, ):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        url = 'https://www.wynikilotto.net.pl/ekstra-pensja/wyniki/'
        html = urllib.request.urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        a = str(soup.find_all('td'))
        p = re.findall(r">(\d\d\d\d)<", a)
        url = 'https://www.wynikilotto.net.pl/ekstra-pensja/wyniki/'+str(p)
        lsource = str(soup.find_all('td'))
        g1 = re.findall(
         r'''>(\d\d\d\d)</td>, <td>(\d\d)[.](\d\d)[.](\d\d\d\d)</td>,
         <td>(\d\d) (\d\d) (\d\d) (\d\d) (\d\d) [+] <b>(\d\d)<''',
         lsource)

        x = 1
        gra = (' ', 'http://www.mbnet.com.pl/ml.txt',
               'http://www.mbnet.com.pl/dl.txt',
               'http://www.mbnet.com.pl/el.txt')
        db_ini = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
                  user, password, host, port, db_base, )
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
        print('updated dfs')

        conn = psycopg2.connect(
         dbname=db_base, user=user, host=host, password=password, )
        print('connected to db4')
        cur = conn.cursor()
        cur.execute(
         '''CREATE TABLE IF NOT EXISTS game4 ("1" INTEGER UNIQUE, "2" INTEGER,
         "3" INTEGER, "4" INTEGER, "5" INTEGER, "6" INTEGER, "7" INTEGER,
         "8" INTEGER, "9" INTEGER, "10" text)''')
        cur.execute(
         '''CREATE UNIQUE INDEX IF NOT EXISTS idx_casenum ON game4 ("1")''')
        cur.executemany(
         '''INSERT INTO game4 ("1","2","3","4","5","6","7","8","9","10") VALUES
         (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ("1") REPLACE''',
         [(v) for v in g1])
        print('updated db ' + str(x) + '...')
        conn.commit()
        conn.close()
        print('connection closed')
