from data.mongoRepository import MongoRepository
from data.monetRepository import MonetRepository
import re

rodando_no_docker = True
qtdPerPage = 5
verbose_level = 2

host_mongo = "localhost"
host_monetdb = "localhost"
if rodando_no_docker:
    host_mongo = "projeto_aplicacao_mongodb"
    host_monetdb = "projeto_aplicacao_monetdb"

mongoConn = MongoRepository(
    connection_string="mongodb://root:root_password@" + host_mongo + ":27017", bd="tcc")

monetdbConn = MonetRepository(
    host_monetdb, "sciphy_dados", "monetdb", "monetdb")


importDictionary = {}
dataflow = {}
dataflow["consulta"] = "select d.id, d.tag from dataflow d order by d.id"
dataflow_execution = {}
dataflow_execution["consulta"] = "select de.id, sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S') as execution_datetime_start, LEAD( sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S') ) over (  order by   de.execution_datetime,   d.id) as execution_datetime_end  from   dataflow d  left join dataflow_execution de on   (d.id = de.df_id) where de.df_id >= #$id$# order by de.df_id limit 1"
dataflow_execution["tipo"] = "primeiro_ou_nulo_sem_paginacao"
dataflow["execution"] = dataflow_execution
data_transformation = {}
data_transformation["consulta"] = "select dt.id,dt.df_id,dt.tag from data_transformation dt"
data_transformation_execution = {}
data_transformation_execution["consulta"] = "select  b.id,  b.dataflow_execution_id,  b.data_transformation_id,  b.execution_datetime_start,  b.execution_datetime_end from  (  select   dte.id,   dte.dataflow_execution_id,   dte.data_transformation_id,   sys.str_to_timestamp(dte.execution_datetime, '%Y-%m-%d %H:%M:%S') as execution_datetime_start,   LEAD( sys.str_to_timestamp(dte.execution_datetime, '%Y-%m-%d %H:%M:%S') ) over (  order by   dte.execution_datetime,   dte.id) as execution_datetime_end  from   data_transformation_execution dte  left join data_transformation dt on   (dt.id = dte.data_transformation_id) ) b where  b.data_transformation_id = #$id$#"
data_transformation_execution["tipo"] = "todos_sem_paginacao"
data_transformation["execution"] = data_transformation_execution
data_transformation_telemetry = {}
data_transformation_telemetry["consulta"] = "select  t.data_transformation_execution_id,  tm.svmem_total,  tm.svmem_total,  tm.svmem_available,  tm.svmem_available,  tm.svmem_used,  tm.svmem_used,  cast( tc.scputimes_user as double) as scputimes_user,  cast( tc.scputimes_system as double) as scputimes_system,  cast( tc.scputimes_idle as double) as scputimes_idle,  cast( tc.scputimes_steal as double) as scputimes_steal,  cast( td.sdiskio_read_bytes as double) as sdiskio_read_bytes,  cast( td.sdiskio_write_bytes as double) as sdiskio_write_bytes,  cast( td.sdiskio_busy_time as double) as sdiskio_busy_time,  cast( td.sswap_total as double) as sswap_total from  telemetry t left join telemetry_cpu tc on  (t.id = tc.telemetry_id) left join telemetry_disk td on  (t.id = td.telemetry_id ) left join telemetry_memory tm on  (t.id = tm.telemetry_id) where t.data_transformation_execution_id = #$id$#"
data_transformation_telemetry["tipo"] = "todos_sem_paginacao"
data_transformation["telemetry"] = data_transformation_telemetry
evolutive_models = {}
evolutive_models["consulta"] = "select  x.program,x.model,x.model_file from  (  select   domrb.model ,   domrb.model_file,   'mrb' program  from   ds_omodelgeneratormodule_mrb domrb union  select    doraxml.model,    doraxml.model_file,    'raxml' program  from    ds_omodelgeneratormodule_raxml doraxml) x"
importDictionary["evolutive_models"] = evolutive_models
importDictionary["dataflow"] = dataflow
importDictionary["data_transformation"] = data_transformation


def insere_documentos(dictionary: dict, nivel: int = 0, dict_father: list = None, chave_insrt: str = None):
    chaves = dictionary.keys()

    result = []

    if 'consulta' in dictionary:
        tipo = "todos"
        if 'tipo' in dictionary:
            tipo = dictionary['tipo']

        result = get_dict_by_consulta(
            dictionary['consulta'], dict_father, chave_insrt, tipo)

    for chave in chaves:
        if(nivel == 0):
            itns_to_insert = insere_documentos(
                dictionary[chave], nivel+1)
            mongoConn.insere(chave, itns_to_insert)
            continue

        if chave != 'consulta' and chave != 'tipo':
            result = insere_documentos(
                dictionary[chave], nivel+1, result, chave)

    return result


def get_dict_by_consulta(consulta_base: str, dict_father: list = None, chave_insrt: str = None, tipo_append: str = "todos_paginado"):
    variaveis = []

    if dict_father != None:
        variaveis = re.findall(r'\#\$(.*?)\$\#', consulta_base)

        retorno = []

        for item_from_dict_father in dict_father:
            nova_consulta = ""

            for variavel in variaveis:
                nova_consulta = consulta_base.replace(
                    '#$'+variavel+'$#', str(item_from_dict_father[variavel]))

            append_result = get_result_consulta(
                nova_consulta, tipo_append)

            if tipo_append == "primeiro_ou_nulo" or tipo_append == "primeiro_ou_nulo_sem_paginacao":
                if len(append_result) > 0:
                    append_result = append_result[0]
                else:
                    append_result = None
            elif tipo_append == "primeiro":
                append_result = append_result[0]

            item_from_dict_father[chave_insrt] = append_result

            retorno.append(item_from_dict_father)

        return retorno
    else:
        return get_result_consulta(consulta_base, tipo_append)


def get_result_consulta(consulta: str, tipo_leitura_consulta: str):
    if(tipo_leitura_consulta == "primeiro_ou_nulo_sem_paginacao" or tipo_leitura_consulta == "todos_sem_paginacao"):
        if verbose_level > 0:
            print('consultando sem paginação: ' + consulta + '\n')
        return tuple_list_to_dictionary(consulta)

    retorno = []

    limit = ' LIMIT ' + str(qtdPerPage) + ' '

    pagina = 1

    ultima_pagina = 1

    ultima_pagina = int(monetdbConn.consultar(
        'SELECT ceil(count(*)/' + str(qtdPerPage) + ') FROM (' + consulta + ') AS x')[0][0])

    if ultima_pagina < 1:
        ultima_pagina = 1

    while(pagina <= ultima_pagina):
        if verbose_level > 0:
            print('percorrendo a pagina ' + str(pagina) + ' de ' +
                  str(ultima_pagina) + ' da consulta ' + consulta + '\n')
        offset = ''

        if(pagina > 1):
            offset = ' OFFSET ' + str((pagina-1) * qtdPerPage) + ' '

        dict_to_insert = tuple_list_to_dictionary(
            'SELECT * FROM (' + consulta + ') x '+limit+offset)

        pagina += 1

        retorno += dict_to_insert

    return retorno


def tuple_list_to_dictionary(consulta: str):
    estrutura = monetdbConn.recupera_estrutura(consulta)
    resultado = monetdbConn.consultar(consulta)

    retorno = []

    for tupla in resultado:
        dicionario = {}
        estutura_campo_indice = 0
        for campo in tupla:
            dicionario[estrutura[estutura_campo_indice].name] = campo
            estutura_campo_indice += 1

        retorno.append(dicionario)

    return retorno


insere_documentos(importDictionary)

monetdbConn.fechar()
