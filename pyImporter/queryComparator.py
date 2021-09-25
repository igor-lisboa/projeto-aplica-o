from datetime import datetime
import json
from data.postgresRepository import PostgresRepository
from data.monetRepository import MonetRepository

rodando_no_docker = False

host_postgres = "localhost"
host_monetdb = "localhost"
if rodando_no_docker:
    host_postgres = "projeto_aplicacao_postgres"
    host_monetdb = "projeto_aplicacao_monetdb"

pgsqlConn = PostgresRepository(
    host_postgres, "public", "postgres", "postgres")

monetdbConn = MonetRepository(
    host_monetdb, "sciphy_dados", "monetdb", "monetdb")


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

t = monetdbConn.recupera_tempo(consultas_monet[0])

conteudo = []

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
    novo_item["postgres"] = str(
        pgsqlConn.recupera_tempo(consultas_postgres[i]))
    novo_item["mongo"] = None
    novo_item["monet"] = str(monetdbConn.recupera_tempo(consultas_monet[i]))
    novo_item["neo4j"] = None

    conteudo.append(novo_item)

f = open("./reports/" + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + ".json", "a")
f.write(json.dumps(conteudo))
f.close()
