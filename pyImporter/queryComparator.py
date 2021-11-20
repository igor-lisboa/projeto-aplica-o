from datetime import datetime
from data.postgresRepository import PostgresRepository
from data.monetRepository import MonetRepository
from data.mongoRepository import MongoRepository

rodando_no_docker = False

host_mongo = "localhost"
host_postgres = "localhost"
host_monetdb = "localhost"
if rodando_no_docker:
    host_mongo = "projeto_aplicacao_mongodb"
    host_postgres = "projeto_aplicacao_postgres"
    host_monetdb = "projeto_aplicacao_monetdb"

pgsqlConn = PostgresRepository(
    host_postgres, "public", "postgres", "postgres")

monetdbConn = MonetRepository(
    host_monetdb, "sciphy_dados", "monetdb", "monetdb")

mongoConn = MongoRepository(
    connection_string="mongodb://root:root_password@" + host_mongo + ":27017", bd="tcc")


consultas_postgres = [
    "select     t.id,     t.next_execution_datetime,     t.execution_datetime,     coalesce(t.next_execution_datetime,     t.execution_datetime) - t.execution_datetime as execution_time from     (     select         d.id,         LEAD( TO_TIMESTAMP(de.execution_datetime, 'YYYY-MM-DD HH24:MI:SS') ) over (     order by         de.execution_datetime,         d.id) as next_execution_datetime,         TO_TIMESTAMP(de.execution_datetime, 'YYYY-MM-DD HH24:MI:SS') as execution_datetime     from         dataflow d     left join dataflow_execution de on         (d.id = de.df_id)     order by         de.execution_datetime,         d.id) t order by     execution_time,     t.id",
    "select     t.data_transformation_id,     t.data_transformation_tag,     sum(coalesce(t.next_execution_datetime,     t.current_execution_datetime) - t.current_execution_datetime) as execution_time from     (     select         dte.id,         dte.dataflow_execution_id,         dte.data_transformation_id,         dt.tag as data_transformation_tag,         TO_TIMESTAMP(dte.execution_datetime, 'YYYY-MM-DD HH24:MI:SS') as current_execution_datetime,         LEAD( TO_TIMESTAMP(dte.execution_datetime, 'YYYY-MM-DD HH24:MI:SS') ) over (     order by         dte.execution_datetime,         dte.id) as next_execution_datetime     from         data_transformation_execution dte     left join data_transformation dt on         (dt.id = dte.data_transformation_id)         ) t group by     t.data_transformation_id,     t.data_transformation_tag;",
    "select     t.data_transformation_execution_id,     dt.tag,     count(t.data_transformation_execution_id) as count_data_transformation_exec,     AVG(tm.svmem_total::float) as avg_svmem_total,     sum(tm.svmem_total::float ) as sum_svmem_total,     AVG(tm.svmem_available::float) as avg_svmem_available,     sum(tm.svmem_available::float) as sum_svmem_available,     AVG(tm.svmem_used::float) as avg_svmem_used,     sum(tm.svmem_used::float) as sum_svmem_used,     AVG( tc.scputimes_user::float) as avg_scputimes_user,     sum(cast( tc.scputimes_user as float)) as sum_scputimes_user,     AVG(cast( tc.scputimes_system as float)) as avg_scputimes_system,     sum(cast( tc.scputimes_system as float)) as sum_scputimes_system,     AVG(cast( tc.scputimes_idle as float)) as avg_scputimes_idle,     sum(cast( tc.scputimes_idle as float)) as sum_scputimes_idle,     AVG(cast( tc.scputimes_steal as float)) as avg_scputimes_steal,     sum(cast( tc.scputimes_steal as float)) as sum_scputimes_steal,     AVG(cast( td.sdiskio_read_bytes as float)) as avg_sdiskio_read_bytes,     sum(cast( td.sdiskio_read_bytes as float)) as sum_sdiskio_read_bytes,     AVG(cast( td.sdiskio_write_bytes as float)) as avg_sdiskio_write_bytes,     sum(cast( td.sdiskio_write_bytes as float)) as sum_sdiskio_write_bytes,     AVG(cast( td.sdiskio_busy_time as float)) as avg_sdiskio_busy_time,     sum(cast( td.sdiskio_busy_time as float)) as sum_sdiskio_busy_time,     AVG(cast( td.sswap_total as float)) as avg_sswap_total,     sum(cast( td.sswap_total as float)) as sum_sswap_total from     data_transformation dt left join telemetry t on     (t.data_transformation_execution_id = dt.id) left join dataflow d on     (dt.df_id = d.id) left join telemetry_cpu tc on     (t.id = tc.telemetry_id) left join telemetry_disk td on     (t.id = td.telemetry_id ) left join telemetry_memory tm on     (t.id = tm.telemetry_id) where     t.data_transformation_execution_id is not null group by     t.data_transformation_execution_id,     dt.tag order by     2 desc",
    "select     uniao.qtd,     uniao.model,     uniao.prog from     (     select         mrb.*     from         (         select             count(*) qtd,             domrb.model,             'mrb' prog         from             ds_omodelgeneratormodule_mrb domrb         group by             domrb.model) mrb union     select         raxml.*     from         (         select             count(*) qtd,             doraxml.model,             'raxml' prog         from             ds_omodelgeneratormodule_raxml doraxml         group by             doraxml.model) raxml) uniao order by 1 desc"
]

consultas_monet = [
    "select  t.id,  t.next_execution_datetime,  t.execution_datetime,  coalesce(t.next_execution_datetime,  t.execution_datetime) - t.execution_datetime as execution_time from  (  select   d.id,   LEAD( sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S') ) over (  order by   de.execution_datetime,   d.id) as next_execution_datetime,   sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S') as execution_datetime  from   dataflow d  left join dataflow_execution de on   (d.id = de.df_id)  order by   de.execution_datetime,   d.id) t order by  execution_time,  t.id",
    "select  t.data_transformation_id,  t.data_transformation_tag,  sum(coalesce(t.next_execution_datetime,  t.current_execution_datetime) - t.current_execution_datetime) as execution_time from  (  select   dte.id,   dte.dataflow_execution_id,   dte.data_transformation_id,   dt.tag as data_transformation_tag,   sys.str_to_timestamp(dte.execution_datetime, '%Y-%m-%d %H:%M:%S') as current_execution_datetime,   LEAD( sys.str_to_timestamp(dte.execution_datetime, '%Y-%m-%d %H:%M:%S') ) over (  order by   dte.execution_datetime,   dte.id) as next_execution_datetime  from   data_transformation_execution dte  left join data_transformation dt on   (dt.id = dte.data_transformation_id)   ) t group by  t.data_transformation_id,  t.data_transformation_tag",
    "select  t.data_transformation_execution_id,  dt.tag,  count(t.data_transformation_execution_id) as count_data_transformation_exec,  avg(tm.svmem_total) as avg_svmem_total,  sum(tm.svmem_total) as sum_svmem_total,  avg(tm.svmem_available) as avg_svmem_available,  sum(tm.svmem_available) as sum_svmem_available,  avg(tm.svmem_used) as avg_svmem_used,  sum(tm.svmem_used) as sum_svmem_used,  avg(cast( tc.scputimes_user as double)) as avg_scputimes_user,  sum(cast( tc.scputimes_user as double)) as sum_scputimes_user,  avg(cast( tc.scputimes_system as double)) as avg_scputimes_system,  sum(cast( tc.scputimes_system as double)) as sum_scputimes_system,  avg(cast( tc.scputimes_idle as double)) as avg_scputimes_idle,  sum(cast( tc.scputimes_idle as double)) as sum_scputimes_idle,  avg(cast( tc.scputimes_steal as double)) as avg_scputimes_steal,  sum(cast( tc.scputimes_steal as double)) as sum_scputimes_steal,  avg(cast( td.sdiskio_read_bytes as double)) as avg_sdiskio_read_bytes,  sum(cast( td.sdiskio_read_bytes as double)) as sum_sdiskio_read_bytes,  avg(cast( td.sdiskio_write_bytes as double)) as avg_sdiskio_write_bytes,  sum(cast( td.sdiskio_write_bytes as double)) as sum_sdiskio_write_bytes,  avg(cast( td.sdiskio_busy_time as double)) as avg_sdiskio_busy_time,  sum(cast( td.sdiskio_busy_time as double)) as sum_sdiskio_busy_time,  avg(cast( td.sswap_total as double)) as avg_sswap_total,  sum(cast( td.sswap_total as double)) as sum_sswap_total from  data_transformation dt left join telemetry t on  (t.data_transformation_execution_id = dt.id) left join dataflow d on  (dt.df_id = d.id) left join telemetry_cpu tc on  (t.id = tc.telemetry_id) left join telemetry_disk td on  (t.id = td.telemetry_id ) left join telemetry_memory tm on  (t.id = tm.telemetry_id) where  t.data_transformation_execution_id is not null group by  t.data_transformation_execution_id,  dt.tag order by  2 desc",
    "select  uniao.qtd,  uniao.model,  uniao.program from  (  select   mrb.*  from   (   select    count(*) qtd,    domrb.model,    'mrb' program   from    ds_omodelgeneratormodule_mrb domrb   group by    domrb.model) mrb union  select   raxml.*  from   (   select    count(*) qtd,    doraxml.model,    'raxml' program   from    ds_omodelgeneratormodule_raxml doraxml   group by    doraxml.model) raxml) uniao order by 1 desc"
]

mongo_pipes = [
    {
        "pipe": [
            {"$project": {
                "_id": 0,
                "id": "$id",
                "next_execution_datetime": {
                    "$ifNull": ["$execution.execution_datetime_end", "$execution.execution_datetime_start"]
                },
                "execution_dattime": {
                    "$ifNull": ["$execution.execution_datetime_start", "$execution.execution_datetime_end"]
                },
                "execution_time": {"$divide": [{"$subtract": ["$execution.execution_datetime_end", "$execution.execution_datetime_start"]}, 1000]}
            }},
            {"$sort": {
                "execution_time": 1,
                "id": 1
            }}],
        "collection": "dataflow"
    },
    {
        "pipe": [
            {"$unwind": {
                "path": "$execution",
                "preserveNullAndEmptyArrays": True
            }},
            {"$project": {
                "data_transformation_id": "$id",
                "data_transformation_tag": "$tag",
                "execution_time_indv": {"$ifNull": [{"$divide": [{"$subtract": [{"$toDate": {"$ifNull": ["$execution.execution_datetime_end", "$execution.execution_datetime_start"]}}, {"$toDate": {"$ifNull": ["$execution.execution_datetime_start", "$execution.execution_datetime_end"]}}]}, 1000]}, 0]}
            }},
            {"$group": {
                "_id": "$data_transformation_id",
                "data_transformation_id": {"$first": "$data_transformation_id"},
                "data_transformation_tag": {"$first": "$data_transformation_tag"},
                "execution_times": {"$sum": "$execution_time_indv"}
            }},
            {"$sort": {
                "_id": 1
            }}],
        "collection": "data_transformation"
    },
    {
        "pipe": [
            {"$unwind": {
                "path": "$telemetry"
            }},
            {"$project": {
                "data_transformation_execution_id": "$id",
                "tag": "$tag",
                "svmem_total": {"$toDouble": "$telemetry.svmem_total"},
                "svmem_available": {"$toDouble": "$telemetry.svmem_available"},
                "svmem_used": {"$toDouble": "$telemetry.svmem_used"},
                "scputimes_user": "$telemetry.scputimes_user",
                "scputimes_system": "$telemetry.scputimes_system",
                "scputimes_idle": "$telemetry.scputimes_idle",
                "scputimes_steal": "$telemetry.scputimes_steal",
                "sdiskio_read_bytes": "$telemetry.sdiskio_read_bytes",
                "sdiskio_write_bytes": "$telemetry.sdiskio_write_bytes",
                "sdiskio_busy_time": "$telemetry.sdiskio_busy_time",
                "sswap_total": "$telemetry.sswap_total"
            }},
            {"$group": {
                "_id": "$data_transformation_execution_id",
                "tag": {"$first": "$tag"},
                "count_data_transformation_exec": {"$sum": 1},
                "avg_svmem_total": {"$avg": "$svmem_total"},
                "sum_svmem_total": {"$sum": "$svmem_total"},
                "avg_svmem_available": {"$avg": "$svmem_available"},
                "sum_svmem_available": {"$sum": "$svmem_available"},
                "avg_svmem_used": {"$avg": "$svmem_used"},
                "sum_svmem_used": {"$sum": "$svmem_used"},
                "avg_scputimes_user": {"$avg": "$scputimes_user"},
                "sum_scputimes_user": {"$sum": "$scputimes_user"},
                "avg_scputimes_system": {"$avg": "$scputimes_system"},
                "sum_scputimes_system": {"$sum": "$scputimes_system"},
                "avg_scputimes_idle": {"$avg": "$scputimes_idle"},
                "sum_scputimes_idle": {"$sum": "$scputimes_idle"},
                "avg_scputimes_steal": {"$avg": "$scputimes_steal"},
                "sum_scputimes_steal": {"$sum": "$scputimes_steal"},
                "avg_sdiskio_read_bytes": {"$avg": "$sdiskio_read_bytes"},
                "sum_sdiskio_read_bytes": {"$sum": "$sdiskio_read_bytes"},
                "avg_sdiskio_write_bytes": {"$avg": "$sdiskio_write_bytes"},
                "sum_sdiskio_write_bytes": {"$sum": "$sdiskio_write_bytes"},
                "avg_sdiskio_busy_time": {"$avg": "$sdiskio_busy_time"},
                "sum_sdiskio_busy_time": {"$sum": "$sdiskio_busy_time"},
                "avg_sswap_total": {"$avg": "$sswap_total"},
                "sum_sswap_total": {"$sum": "$sswap_total"}
            }},
            {"$sort": {
                "tag": -1
            }}
        ],
        "collection": "data_transformation"
    },
    {
        "pipe": [
            {"$group": {
                "_id": {
                    "model": "$model",
                    "program": "$program"
                },
                "qtd": {"$sum": 1}
            }},
            {"$project": {
                "_id": 0,
                "qtd": "$qtd",
                "model": "$_id.model",
                "program": "$_id.program"
            }},
            {"$sort": {
                "qtd": -1
            }}],
        "collection": "evolutive_models"
    }
]

for i in range(0, 3):
    novo_item = {}

    texto = ""
    if(i == 0):
        texto = "consulta de tempos de execucao para cada execucao realizada"
    elif(i == 1):
        texto = "consulta de duracao de execucao por transformacao"
    elif(i == 2):
        texto = "Consulta para identificar consumo de recurso por transformacao (relacionando telemetry data_transformation_execution_id com data_transformation) e por dataflow"
    elif(i == 3):
        texto = "quantitativo de modelos evolutivos calculados"
    else:
        texto = "ERRO"

    novo_item["consulta"] = texto
    novo_item["mongo"] = mongoConn.recupera_tempo(
        mongo_pipes[i]["collection"], mongo_pipes[i]["pipe"]).microseconds
    novo_item["postgres"] = pgsqlConn.recupera_tempo(
        consultas_postgres[i]).microseconds
    novo_item["monet"] = monetdbConn.recupera_tempo(
        consultas_monet[i]).microseconds
    novo_item["neo4j"] = None
    novo_item["created_at"] = datetime.now()

    mongoConn.insere("reports", [novo_item])
