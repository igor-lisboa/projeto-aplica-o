import pymonetdb
from pymonetdb.sql.connections import Connection


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

    def fechar(self):
        self._db.close()
