import pymonetdb
from pymonetdb.sql.connections import Connection
import datetime


class MonetRepository(object):
    _db: Connection

    def __init__(self, mhost: str, db: str, usr: str, pwd: str):
        self._db = pymonetdb.connect(
            username=usr, password=pwd, hostname=mhost, database=db)

    def manipular(self, sql: str, bind: list = []):
        cur = self._db.cursor()
        cur.execute(sql, bind)
        cur.close()
        self._db.commit()

    def consultar(self, sql: str, bind: list = []):
        rs = None
        cur = self._db.cursor()
        cur.execute(sql, bind)
        rs = cur.fetchall()
        cur.close()
        return rs

    def recupera_estrutura(self, sql: str, bind: list = []):
        cur = self._db.cursor()
        cur.execute(sql, bind)
        estrutura = cur.description
        cur.close()
        return estrutura

    def recupera_tempo(self, sql: str, bind: list = []):
        init_time = datetime.datetime.now()
        self.consultar(sql, bind)
        end_time = datetime.datetime.now()

        return end_time - init_time

    def fechar(self):
        self._db.close()
