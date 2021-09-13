import pymonetdb
import json
from pymonetdb.sql.cursors import Cursor
from data.postgresRepository import PostgresRepository

qtdPerPage = 10

pgsqlConn = PostgresRepository("localhost", "public", "postgres", "postgres")

# import the SQL module
# set up a connection. arguments below are the defaults
monetdbConn = pymonetdb.connect(
    username="monetdb", password="monetdb", hostname="localhost", database="sciphy_dados")

# create a cursor
cursor = monetdbConn.cursor()

# increase the rows fetched to increase performance (optional)
cursor.arraysize = 100


def percorre_tabelas(cursor: Cursor, consulta: str):
    limit = ' LIMIT ' + str(qtdPerPage) + ' '

    pagina = 1

    tabela = consulta.split()[-1]

    esquema_postgres = "public"

    insert_query = "INSERT INTO " + esquema_postgres + "."+tabela
    insert_query_colunas = ""

    cursor.execute(
        'SELECT ceil(count(*)/' + str(qtdPerPage) + ') FROM (' + consulta + ') x')
    ultima_pagina = int(cursor.fetchone()[0])

    while(pagina <= ultima_pagina):
        print('percorrendo a pagina ' + str(pagina) + ' de ' +
              str(ultima_pagina) + ' da consulta ' + consulta + '\n')
        offset = ''

        if(pagina > 1):
            offset = ' OFFSET ' + str((pagina-1) * qtdPerPage) + ' '

        cursor.execute(consulta+limit+offset)
        resultado = cursor.fetchall()

        if len(resultado) > 0:

            values_bind_consulta = ""

            if(pagina == 1):

                for coluna in cursor.description:

                    if insert_query_colunas != "":
                        insert_query_colunas += ","
                        values_bind_consulta += ","

                    insert_query_colunas += coluna[0]
                    values_bind_consulta += "%s"

                insert_query += "("+insert_query_colunas + \
                    ") VALUES "

                values_bind_consulta = "("+values_bind_consulta+")"

            bind = []

            values_consulta = ""

            for tupla in resultado:
                for value in tupla:

                    if value == 'null':
                        value = None

                    bind.append(value)

                if values_consulta != "":
                    values_consulta += ","

                values_consulta += values_bind_consulta

            insert_query += values_consulta

            print("Executando a query: " + insert_query +
                  " no POSTGRES, com os valores: " + json.dumps(bind) + "\n\n")

            pgsqlConn.manipular(insert_query, bind)

        pagina += 1


tabelas = [
    'SELECT id,tag,user_id FROM dataflow',
    'SELECT id,df_id,tag,program_id FROM data_transformation',
    'SELECT version,df_id FROM dataflow_version',
    'SELECT id,df_id,tag FROM data_set',
    'SELECT id,previous_dt_id,next_dt_id,ds_id FROM data_dependency',
    'SELECT id,ds_id,extractor_id,name,type FROM attribute',
    'SELECT id,identifier,df_version,dt_id,status,workspace,computing_resource,output_msg,error_msg FROM task',
    'SELECT id,task_id,subtask_id,method,description,starttime,endtime,invocation FROM performance',
    'SELECT id,execution_datetime,df_id,physical_machine_id,virtual_machine_id FROM dataflow_execution',
    'SELECT id,dataflow_execution_id,data_transformation_id,execution_datetime FROM data_transformation_execution',
    'SELECT id,task_id,captured_timestamp,captured_interval,data_transformation_execution_id FROM telemetry',
    'SELECT id,telemetry_id,consumption_timestamp,scputimes_user,scputimes_system,scputimes_idle,scputimes_steal FROM telemetry_cpu',
    'SELECT id,telemetry_id,consumption_timestamp,sdiskio_read_bytes,sdiskio_write_bytes,sdiskio_busy_time,sswap_total,sswap_used FROM telemetry_disk',
    'SELECT id,telemetry_id,consumption_timestamp,svmem_total,svmem_available,svmem_used FROM telemetry_memory',
    'SELECT id,removepipemodule_raxml_task_id,inputfile FROM ds_iremovepipemodule_raxml',
    'SELECT id,removepipemodule_raxml_task_id,cleanedfile FROM ds_oremovepipemodule_raxml',
    'SELECT id,alignmentmodule_raxml_task_id,directory,cleaned_seq FROM ds_ialignmentmodule_raxml',
    'SELECT id,alignmentmodule_raxml_task_id,alignmenttype,directory,alignedcode FROM ds_oalignmentmodule_raxml',
    'SELECT id,convertermodule_raxml_task_id,dirin,inputfile,trimmer FROM ds_iconvertermodule_raxml',
    'SELECT id,convertermodule_raxml_task_id,nxs_file,phy_file FROM ds_oconvertermodule_raxml',
    'SELECT id,modelgeneratormodule_raxml_task_id,alignedfile FROM ds_imodelgeneratormodule_raxml',
    'SELECT id,modelgeneratormodule_raxml_task_id,model,model_file FROM ds_omodelgeneratormodule_raxml',
    'SELECT id,programexecutemodule_raxml_task_id,program FROM ds_iprogramexecutemodule_raxml',
    'SELECT id,programexecutemodule_raxml_task_id,program,mbout,param_mbayes,nxs_ckp,con_tre,parts FROM ds_oprogramexecutemodule_raxml',
    'SELECT id,removepipemodule_mrb_task_id,inputfile FROM ds_iremovepipemodule_mrb',
    'SELECT id,removepipemodule_mrb_task_id,cleanedfile FROM ds_oremovepipemodule_mrb',
    'SELECT id,alignmentmodule_mrb_task_id,directory,cleaned_seq FROM ds_ialignmentmodule_mrb',
    'SELECT id,alignmentmodule_mrb_task_id,alignmenttype,directory,alignedcode FROM ds_oalignmentmodule_mrb',
    'SELECT id,convertermodule_mrb_task_id,dirin,inputfile,trimmer FROM ds_iconvertermodule_mrb',
    'SELECT id,convertermodule_mrb_task_id,nxs_file,phy_file FROM ds_oconvertermodule_mrb',
    'SELECT id,modelgeneratormodule_mrb_task_id,alignedfile FROM ds_imodelgeneratormodule_mrb',
    'SELECT id,modelgeneratormodule_mrb_task_id,model,model_file FROM ds_omodelgeneratormodule_mrb',
    'SELECT id,programexecutemodule_mrb_task_id,program FROM ds_iprogramexecutemodule_mrb',
    'SELECT id,programexecutemodule_mrb_task_id,program,mbout,param_mbayes,nxs_ckp,con_tre,parts FROM ds_oprogramexecutemodule_mrb'
]

for consulta in tabelas:
    try:
        percorre_tabelas(cursor, consulta)
    except Exception as ex:
        print("Erro: "+str(ex) + " na consulta: "+consulta + "\n\n\n")
        raise ex

# define FKs
set_fks = "ALTER TABLE \"public\".\"attribute\" ADD CONSTRAINT \"attribute_extractor_id_fkey\" FOREIGN KEY (\"extractor_id\") REFERENCES \"public\".\"extractor\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"data_dependency\" ADD CONSTRAINT \"data_dependency_ds_id_fkey\" FOREIGN KEY (\"ds_id\") REFERENCES \"public\".\"data_set\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"data_dependency\" ADD CONSTRAINT \"data_dependency_next_dt_id_fkey\" FOREIGN KEY (\"next_dt_id\") REFERENCES \"public\".\"data_transformation\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE;"
set_fks += "ALTER TABLE \"public\".\"data_dependency\" ADD CONSTRAINT \"data_dependency_previous_dt_id_fkey\" FOREIGN KEY (\"previous_dt_id\") REFERENCES \"public\".\"data_transformation\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"data_set\" ADD CONSTRAINT \"data_set_df_id_fkey\" FOREIGN KEY (\"df_id\") REFERENCES \"public\".\"dataflow\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"data_transformation\" ADD CONSTRAINT \"data_transformation_df_id_fkey\" FOREIGN KEY (\"df_id\") REFERENCES \"public\".\"dataflow\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE;"
set_fks += "ALTER TABLE \"public\".\"data_transformation\" ADD CONSTRAINT \"data_transformation_program_id_fkey\" FOREIGN KEY (\"program_id\") REFERENCES \"public\".\"program\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"data_transformation_execution\" ADD CONSTRAINT \"data_transformation_execution_data_transformation_id_fkey\" FOREIGN KEY (\"data_transformation_id\") REFERENCES \"public\".\"data_transformation\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"data_transformation_execution\" ADD CONSTRAINT \"data_transformation_execution_dataflow_execution_id_fkey\" FOREIGN KEY (\"dataflow_execution_id\") REFERENCES \"public\".\"dataflow_execution\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE;"
set_fks += "ALTER TABLE \"public\".\"dataflow\" ADD CONSTRAINT \"dataflow_user_id_fkey\" FOREIGN KEY (\"user_id\") REFERENCES \"public\".\"user_table\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"dataflow_execution\" ADD CONSTRAINT \"dataflow_execution_df_id_fkey\" FOREIGN KEY (\"df_id\") REFERENCES \"public\".\"dataflow\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"dataflow_execution\" ADD CONSTRAINT \"dataflow_execution_physical_machine_id_fkey\" FOREIGN KEY (\"physical_machine_id\") REFERENCES \"public\".\"physical_machine\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"dataflow_execution\" ADD CONSTRAINT \"dataflow_execution_virtual_machine_id_fkey\" FOREIGN KEY (\"virtual_machine_id\") REFERENCES \"public\".\"virtual_machine\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"dataflow_version\" ADD CONSTRAINT \"dataflow_version_df_id_fkey\" FOREIGN KEY (\"df_id\") REFERENCES \"public\".\"dataflow\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_ialignmentmodule_mrb\" ADD CONSTRAINT \"ds_ialignmentmodule_mrb_alignmentmodule_mrb_task_id_fkey\" FOREIGN KEY (\"alignmentmodule_mrb_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE;"
set_fks += "ALTER TABLE \"public\".\"ds_ialignmentmodule_raxml\" ADD CONSTRAINT \"ds_ialignmentmodule_raxml_alignmentmodule_raxml_task_id_fkey\" FOREIGN KEY (\"alignmentmodule_raxml_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_iconvertermodule_mrb\" ADD CONSTRAINT \"ds_iconvertermodule_mrb_convertermodule_mrb_task_id_fkey\" FOREIGN KEY (\"convertermodule_mrb_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_iconvertermodule_raxml\" ADD CONSTRAINT \"ds_iconvertermodule_raxml_convertermodule_raxml_task_id_fkey\" FOREIGN KEY (\"convertermodule_raxml_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_imodelgeneratormodule_mrb\" ADD CONSTRAINT \"ds_imodelgeneratormodule_mrb_modelgeneratormodule_mrb_task_id_fkey\" FOREIGN KEY (\"modelgeneratormodule_mrb_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_imodelgeneratormodule_raxml\" ADD CONSTRAINT \"ds_imodelgeneratormodule_raxml_modelgeneratormodule_raxml_task_id_fkey\" FOREIGN KEY (\"modelgeneratormodule_raxml_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE;"
set_fks += "ALTER TABLE \"public\".\"ds_iprogramexecutemodule_mrb\" ADD CONSTRAINT \"ds_iprogramexecutemodule_mrb_programexecutemodule_mrb_task_id_fkey\" FOREIGN KEY (\"programexecutemodule_mrb_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_iprogramexecutemodule_raxml\" ADD CONSTRAINT \"ds_iprogramexecutemodule_raxml_programexecutemodule_raxml_task_id_fkey\" FOREIGN KEY (\"programexecutemodule_raxml_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_iremovepipemodule_mrb\" ADD CONSTRAINT \"ds_iremovepipemodule_mrb_removepipemodule_mrb_task_id_fkey\" FOREIGN KEY (\"removepipemodule_mrb_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_iremovepipemodule_raxml\" ADD CONSTRAINT \"ds_iremovepipemodule_raxml_removepipemodule_raxml_task_id_fkey\" FOREIGN KEY (\"removepipemodule_raxml_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_itelemetry_mrb\" ADD CONSTRAINT \"ds_itelemetry_mrb_telemetrymodule_mrb_task_id_fkey\" FOREIGN KEY (\"telemetrymodule_mrb_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_itelemetry_raxml\" ADD CONSTRAINT \"ds_itelemetry_raxml_telemetrymodule_raxml_task_id_fkey\" FOREIGN KEY (\"telemetrymodule_raxml_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_ivalidationmodule_mrb\" ADD CONSTRAINT \"ds_ivalidationmodule_mrb_validationmodule_mrb_task_id_fkey\" FOREIGN KEY (\"validationmodule_mrb_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_ivalidationmodule_raxml\" ADD CONSTRAINT \"ds_ivalidationmodule_raxml_validationmodule_raxml_task_id_fkey\" FOREIGN KEY (\"validationmodule_raxml_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE;"
set_fks += "ALTER TABLE \"public\".\"ds_oalignmentmodule_mrb\" ADD CONSTRAINT \"ds_oalignmentmodule_mrb_alignmentmodule_mrb_task_id_fkey\" FOREIGN KEY (\"alignmentmodule_mrb_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_oalignmentmodule_raxml\" ADD CONSTRAINT \"ds_oalignmentmodule_raxml_alignmentmodule_raxml_task_id_fkey\" FOREIGN KEY (\"alignmentmodule_raxml_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_oconvertermodule_mrb\" ADD CONSTRAINT \"ds_oconvertermodule_mrb_convertermodule_mrb_task_id_fkey\" FOREIGN KEY (\"convertermodule_mrb_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_oconvertermodule_raxml\" ADD CONSTRAINT \"ds_oconvertermodule_raxml_convertermodule_raxml_task_id_fkey\" FOREIGN KEY (\"convertermodule_raxml_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_omodelgeneratormodule_mrb\" ADD CONSTRAINT \"ds_omodelgeneratormodule_mrb_modelgeneratormodule_mrb_task_id_fkey\" FOREIGN KEY (\"modelgeneratormodule_mrb_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE;"
set_fks += "ALTER TABLE \"public\".\"ds_omodelgeneratormodule_raxml\" ADD CONSTRAINT \"ds_omodelgeneratormodule_raxml_modelgeneratormodule_raxml_task_id_fkey\" FOREIGN KEY (\"modelgeneratormodule_raxml_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_oprogramexecutemodule_mrb\" ADD CONSTRAINT \"ds_oprogramexecutemodule_mrb_programexecutemodule_mrb_task_id_fkey\" FOREIGN KEY (\"programexecutemodule_mrb_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_oprogramexecutemodule_raxml\" ADD CONSTRAINT \"ds_oprogramexecutemodule_raxml_programexecutemodule_raxml_task_id_fkey\" FOREIGN KEY (\"programexecutemodule_raxml_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_oremovepipemodule_mrb\" ADD CONSTRAINT \"ds_oremovepipemodule_mrb_removepipemodule_mrb_task_id_fkey\" FOREIGN KEY (\"removepipemodule_mrb_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE;"
set_fks += "ALTER TABLE \"public\".\"ds_oremovepipemodule_raxml\" ADD CONSTRAINT \"ds_oremovepipemodule_raxml_removepipemodule_raxml_task_id_fkey\" FOREIGN KEY (\"removepipemodule_raxml_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_otelemetry_mrb\" ADD CONSTRAINT \"ds_otelemetry_mrb_telemetrymodule_mrb_task_id_fkey\" FOREIGN KEY (\"telemetrymodule_mrb_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_otelemetry_raxml\" ADD CONSTRAINT \"ds_otelemetry_raxml_telemetrymodule_raxml_task_id_fkey\" FOREIGN KEY (\"telemetrymodule_raxml_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_ovalidationmodule_mrb\" ADD CONSTRAINT \"ds_ovalidationmodule_mrb_validationmodule_mrb_task_id_fkey\" FOREIGN KEY (\"validationmodule_mrb_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"ds_ovalidationmodule_raxml\" ADD CONSTRAINT \"ds_ovalidationmodule_raxml_validationmodule_raxml_task_id_fkey\" FOREIGN KEY (\"validationmodule_raxml_task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE;"
set_fks += "ALTER TABLE \"public\".\"epoch\" ADD CONSTRAINT \"epoch_data_transformation_execution_id_fkey\" FOREIGN KEY (\"data_transformation_execution_id\") REFERENCES \"public\".\"data_transformation_execution\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"epoch\" ADD CONSTRAINT \"epoch_task_id_fkey\" FOREIGN KEY (\"task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"extractor\" ADD CONSTRAINT \"extractor_ds_id_fkey\" FOREIGN KEY (\"ds_id\") REFERENCES \"public\".\"data_set\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"extractor_combination\" ADD CONSTRAINT \"extractor_combination_ds_id_fkey\" FOREIGN KEY (\"ds_id\") REFERENCES \"public\".\"data_set\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"extractor_combination\" ADD CONSTRAINT \"extractor_combination_inner_ext_id_fkey\" FOREIGN KEY (\"inner_ext_id\") REFERENCES \"public\".\"extractor\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"extractor_combination\" ADD CONSTRAINT \"extractor_combination_outer_ext_id_fkey\" FOREIGN KEY (\"outer_ext_id\") REFERENCES \"public\".\"extractor\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"file\" ADD CONSTRAINT \"file_id_file_type_fkey\" FOREIGN KEY (\"id_file_type\") REFERENCES \"public\".\"file_type\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE;"
set_fks += "ALTER TABLE \"public\".\"file_transformation_execution\" ADD CONSTRAINT \"file_transformation_execution_data_transformation_execution_id_fkey\" FOREIGN KEY (\"data_transformation_execution_id\") REFERENCES \"public\".\"data_transformation_execution\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"file_transformation_execution\" ADD CONSTRAINT \"file_transformation_execution_file_id_fkey\" FOREIGN KEY (\"file_id\") REFERENCES \"public\".\"file\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"performance\" ADD CONSTRAINT \"performance_task_id_fkey\" FOREIGN KEY (\"task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"physical_machine\" ADD CONSTRAINT \"physical_machine_owner_user_id_fkey\" FOREIGN KEY (\"owner_user_id\") REFERENCES \"public\".\"user_table\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"task\" ADD CONSTRAINT \"task_df_version_fkey\" FOREIGN KEY (\"df_version\") REFERENCES \"public\".\"dataflow_version\" (\"version\") ON DELETE CASCADE ON UPDATE CASCADE;"
set_fks += "ALTER TABLE \"public\".\"task\" ADD CONSTRAINT \"task_dt_id_fkey\" FOREIGN KEY (\"dt_id\") REFERENCES \"public\".\"data_transformation\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"telemetry\" ADD CONSTRAINT \"telemetry_data_transformation_execution_id_fkey\" FOREIGN KEY (\"data_transformation_execution_id\") REFERENCES \"public\".\"data_transformation_execution\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"telemetry\" ADD CONSTRAINT \"telemetry_task_id_fkey\" FOREIGN KEY (\"task_id\") REFERENCES \"public\".\"task\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"telemetry_cpu\" ADD CONSTRAINT \"telemetry_cpu_telemetry_id_fkey\" FOREIGN KEY (\"telemetry_id\") REFERENCES \"public\".\"telemetry\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"telemetry_disk\" ADD CONSTRAINT \"telemetry_disk_telemetry_id_fkey\" FOREIGN KEY (\"telemetry_id\") REFERENCES \"public\".\"telemetry\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"telemetry_memory\" ADD CONSTRAINT \"telemetry_memory_telemetry_id_fkey\" FOREIGN KEY (\"telemetry_id\") REFERENCES \"public\".\"telemetry\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE;"
set_fks += "ALTER TABLE \"public\".\"telemetry_network\" ADD CONSTRAINT \"telemetry_network_telemetry_id_fkey\" FOREIGN KEY (\"telemetry_id\") REFERENCES \"public\".\"telemetry\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"use_program\" ADD CONSTRAINT \"use_program_dt_id_fkey\" FOREIGN KEY (\"dt_id\") REFERENCES \"public\".\"data_transformation\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"use_program\" ADD CONSTRAINT \"use_program_program_id_fkey\" FOREIGN KEY (\"program_id\") REFERENCES \"public\".\"program\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE; ALTER TABLE \"public\".\"virtual_machine\" ADD CONSTRAINT \"virtual_machine_physical_machine_id_fkey\" FOREIGN KEY (\"physical_machine_id\") REFERENCES \"public\".\"physical_machine\" (\"id\") ON DELETE CASCADE ON UPDATE CASCADE;"

print("Executando a query pra inserir as FK's: " + set_fks)
pgsqlConn.manipular(set_fks)

pgsqlConn.fechar()
