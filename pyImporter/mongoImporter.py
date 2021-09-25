from data.mongoRepository import MongoRepository
from data.monetRepository import MonetRepository

rodando_no_docker = False

host_mongo = "localhost"
host_monetdb = "localhost"
if rodando_no_docker:
    host_mongo = "projeto_aplicacao_mongodb"
    host_monetdb = "projeto_aplicacao_monetdb"

mongoConn = MongoRepository(
    connection_string="mongodb://root:root_password@" + host_mongo + ":27017", bd="tcc")

monetdbConn = MonetRepository(
    host_monetdb, "sciphy_dados", "monetdb", "monetdb")


importArr = {}

dataflow = {}
dataflow["consulta"] = "select   d.id,   d.tag,   sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S') as execution_datetime  from   dataflow d  left join dataflow_execution de on   (d.id = de.df_id)  order by   de.execution_datetime,   d.id"

importArr["dataflow"] = dataflow
