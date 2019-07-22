import psycopg2
import pandas
import urllib.request.urlopen
from bs4 import BeautifulSoup
import re
import ssl
from sqlalchemy import create_engine


class Updatedb(object):
    ''' Klasa aktualizująca bazę danych randomizera '''

    def __init__(self):
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
        self.g1 = re.findall(
         r'''>(\d\d\d\d)</td>, <td>(\d\d)[.](\d\d)[.](\d\d\d\d)</td>,
         <td>(\d\d) (\d\d) (\d\d) (\d\d) (\d\d) [+] <b>(\d\d)<''',
         lsource)

    def connect(self, user, password, host, port, db_base, db, ):
        x = 0
        gra = (' ', 'http://www.mbnet.com.pl/ml.txt',
               'http://www.mbnet.com.pl/dl.txt',
               'http://www.mbnet.com.pl/el.txt')
        query = 'game{0}, engine,if_exists="replace",index=False'.format(x)
        db_ini = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
                  user, password, host, port, db_base, )
        engine = create_engine(db_ini)
        while x < 4:
            x = x + 1
            df = pandas.read_csv(gra[x], header=None, sep='[., ]',
                                 engine='python')
            df.to_sql(query)
            conn = engine.raw_connection()
            cur = self.conn.cursor()
            self.conn.commit()

        conn = psycopg2.connect(db)
        cur = conn.cursor()
        cur.execute(
         '''CREATE TABLE IF NOT EXISTS game4 ("1" INTEGER UNIQUE, "2" INTEGER,
         "3" INTEGER, "4" INTEGER, "5" INTEGER, "6" INTEGER, "7" INTEGER,
         "8" INTEGER, "9" INTEGER, "10" text)''')
        cur.execute(
         'CREATE UNIQUE INDEX IF NOT EXISTS idx_casenum ON game4 ("1")')
        cur.executemany(
         '''INSERT INTO game4 ("1","2","3","4","5","6","7","8","9","10") VALUES
         (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ("1") DO NOTHING''',
         [(v) for v in self.g1])
        self.conn.commit()

    def __del__(self):
        self.conn.close()
