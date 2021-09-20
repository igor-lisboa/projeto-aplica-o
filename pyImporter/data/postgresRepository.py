import psycopg2


class PostgresRepository(object):
    _db = None

    def __init__(self, mhost: str, db: str, usr: str, pwd: str):
        self._db = psycopg2.connect(
            host=mhost, database=db, user=usr,  password=pwd)

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

    def fechar(self):
        self._db.close()
