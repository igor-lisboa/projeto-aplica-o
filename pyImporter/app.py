import pymonetdb
from pymonetdb.sql.cursors import Cursor

qtdPerPage = 10

# import the SQL module
# set up a connection. arguments below are the defaults
monetdbConn = pymonetdb.connect(
    username="monetdb", password="monetdb", hostname="projeto_aplicacao_monetdb", database="sciphy_dados")

# create a cursor
cursor = monetdbConn.cursor()

# increase the rows fetched to increase performance (optional)
cursor.arraysize = 100


def percorre_tabelas(cursor: Cursor, consulta: str):
    limit = ' LIMIT ' + str(qtdPerPage) + ' '

    pagina = 1

    cursor.execute(
        'SELECT ceil(count(*)/' + str(qtdPerPage) + ') FROM (' + consulta + ') x')
    ultima_pagina = int(cursor.fetchone()[0])

    while(pagina <= ultima_pagina):
        print('percorrendo a pagina ' + str(pagina) + '\n')
        offset = ''

        if(pagina > 1):
            offset = ' OFFSET ' + str((pagina-1) * qtdPerPage) + ' '

        cursor.execute(consulta+limit+offset)
        cursor.fetchall()

        if(pagina == 1):
            # Show the table meta data
            cursor.description

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
    percorre_tabelas(cursor, consulta)
