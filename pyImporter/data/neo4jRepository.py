from neo4j import GraphDatabase
import datetime


class Neo4jRepository:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def manipular(self, query: str, parameters: object):
        with self.driver.session() as session:
            session.run(query, parameters)

    def consultar(self, query: str, parameters: object):
        rs = None
        with self.driver.session() as session:
            resultado = session.run(query, parameters)
            rs = resultado.data()
        return rs

    def recupera_tempo(self, query: str, parameters: object):
        init_time = datetime.datetime.now()
        self.consultar(query, parameters)
        end_time = datetime.datetime.now()

        return end_time - init_time

    def fechar(self):
        self.driver.close()
