from data.neo4jRepository import Neo4jRepository
from data.monetRepository import MonetRepository
import re
import json
from datetime import date

rodando_no_docker = True
qtdPerPage = 5
verbose_level = 2

host_neo4j = "neo4j:bolt://localhost"
host_monetdb = "localhost"
if rodando_no_docker:
    host_neo4j = "bolt://projeto_aplicacao_neo4j"
    host_monetdb = "projeto_aplicacao_monetdb"

neo4jConn = Neo4jRepository(uri=host_neo4j + ":7687/",
                            user="neo4j", password="senha_neo4j")

monetdbConn = MonetRepository(
    host_monetdb, "sciphy_dados", "monetdb", "monetdb")


importDictionary = {}
dataflow = {}
dataflow["consulta"] = "select d.id, d.tag from dataflow d order by d.id"
dataflow_execution = {}
dataflow_execution["consulta"] = "select de.id, de.df_id, sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S') as execution_datetime_start, coalesce(LEAD( sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S') ) over (  order by   de.execution_datetime,   d.id),sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S')) as execution_datetime_end  from   dataflow d  left join dataflow_execution de on   (d.id = de.df_id) where de.df_id >= #$id$# order by de.df_id limit 1"
dataflow_execution["tipo"] = "primeiro_ou_nulo_sem_paginacao"
dataflow["[:PERFORMED:][#id#][$id$][&DataflowExecution&]"] = dataflow_execution
data_transformation = {}
data_transformation["consulta"] = "select dt.id,dt.df_id,dt.tag from data_transformation dt"
data_transformation_execution = {}
data_transformation_execution["consulta"] = "select  b.id,  b.dataflow_execution_id,  b.data_transformation_id,  b.execution_datetime_start,  b.execution_datetime_end from  (  select   dte.id,   dte.dataflow_execution_id,   dte.data_transformation_id,   sys.str_to_timestamp(dte.execution_datetime, '%Y-%m-%d %H:%M:%S') as execution_datetime_start,   LEAD( sys.str_to_timestamp(dte.execution_datetime, '%Y-%m-%d %H:%M:%S') ) over (  order by   dte.execution_datetime,   dte.id) as execution_datetime_end  from   data_transformation_execution dte  left join data_transformation dt on   (dt.id = dte.data_transformation_id) ) b where  b.data_transformation_id = #$id$#"
data_transformation_execution["tipo"] = "todos_sem_paginacao"
data_transformation["[:PERFORMED:][#id#][$id$][&DataTransformationExecution&]"] = data_transformation_execution
data_transformation_telemetry = {}
data_transformation_telemetry["consulta"] = "select t.id , t.data_transformation_execution_id,  tm.svmem_total,  tm.svmem_total,  tm.svmem_available,  tm.svmem_available,  tm.svmem_used,  tm.svmem_used,  cast( tc.scputimes_user as double) as scputimes_user,  cast( tc.scputimes_system as double) as scputimes_system,  cast( tc.scputimes_idle as double) as scputimes_idle,  cast( tc.scputimes_steal as double) as scputimes_steal,  cast( td.sdiskio_read_bytes as double) as sdiskio_read_bytes,  cast( td.sdiskio_write_bytes as double) as sdiskio_write_bytes,  cast( td.sdiskio_busy_time as double) as sdiskio_busy_time,  cast( td.sswap_total as double) as sswap_total from  telemetry t left join telemetry_cpu tc on  (t.id = tc.telemetry_id) left join telemetry_disk td on  (t.id = td.telemetry_id ) left join telemetry_memory tm on  (t.id = tm.telemetry_id) where t.data_transformation_execution_id = #$id$#"
data_transformation_telemetry["tipo"] = "todos_sem_paginacao"
data_transformation["[:COLLECTED:][#id#][$id$][&Telemetry&]"] = data_transformation_telemetry
evolutive_models = {}
evolutive_models["consulta"] = "select  x.program,x.model,x.model_file from  (  select   domrb.model ,   domrb.model_file,   'mrb' program  from   ds_omodelgeneratormodule_mrb domrb union  select    doraxml.model,    doraxml.model_file,    'raxml' program  from    ds_omodelgeneratormodule_raxml doraxml) x"
importDictionary["EvolutiveModels"] = evolutive_models
importDictionary["Dataflow"] = dataflow
importDictionary["DataTransformation"] = data_transformation


dataDictionary = {}


def fill_data_dictionary(dictionary: dict, nivel: int = 0, dict_father: list = None, chave_insrt: str = None):
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
            itns_to_insert = fill_data_dictionary(
                dictionary[chave], nivel+1)
            dataDictionary[chave] = itns_to_insert
            continue

        if chave != 'consulta' and chave != 'tipo':
            result = fill_data_dictionary(
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
        'SELECT ceil(count(*)/' + str(qtdPerPage) + ') FROM (' + consulta + ') AS x')[0][0]) + 1

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


def insert_neo4j_from_data_dictionary(data_dictionary: dict, level: int = 0, node_label: str = None, father_node: dict = None, relationship_label: str = None, father_key_comp: str = None, child_key_comp: str = None, label_relationship_father: str = None):
    relationship_keys = []
    dict_to_make_node = {}

    for key in data_dictionary.keys():
        if verbose_level > 0:
            print('verificando key: ' + str(key) +
                  ' do dict, com o nivel '+str(level)+' e com node label do pai de '+str(node_label)+'\n')
        if(level == 0):
            if isinstance(data_dictionary[key], list):
                for item in data_dictionary[key]:
                    insert_neo4j_from_data_dictionary(
                        item, level+1, key, father_node, relationship_label, father_key_comp, child_key_comp, label_relationship_father)
            else:
                insert_neo4j_from_data_dictionary(
                    data_dictionary[key], level+1, key, father_node, relationship_label, father_key_comp, child_key_comp, label_relationship_father)
        else:
            if(key[0] != '['):
                dict_to_make_node[key] = data_dictionary[key]
            else:
                relationship_keys.append(key)

    if len(dict_to_make_node) > 0:
        command_create_string = "CREATE (n:" + node_label + " $props)"
        command_create_params = {
            'props': dict_to_make_node
        }

        if verbose_level >= 2:
            print("Preparando pra executar o seguinte comando de CREATE ::::>\n"+json.dumps({
                'command': command_create_string,
                'params': command_create_params
            }, indent=4,
                sort_keys=True, default=str))

        neo4jConn.manipular(command_create_string, command_create_params)

        if relationship_label != None:
            command_match_string = "MATCH   (a:"+label_relationship_father+"),   (b:"+node_label+")  WHERE toString(a."+father_key_comp+") = '"+str(
                father_node[father_key_comp])+"' AND toString(b."+child_key_comp+") = '" + str(dict_to_make_node[child_key_comp]) + "'      CREATE (a)-[r:"+relationship_label+"]->(b)  RETURN type(r)"

            if verbose_level >= 2:
                print("Preparando pra executar o seguinte comando de MATCH ::::>\n" +
                      command_match_string)

            neo4jConn.manipular(command_match_string, {})

        for especial_key in relationship_keys:
            # [:collected:][#id#][$data_transformation_execution_id$][&Telemetry&]
            relationship = re.findall(r'\[\:(.*?)\:\]', especial_key)[0]
            father_key = re.findall(r'\[\#(.*?)\#\]', especial_key)[0]
            child_key = re.findall(r'\[\$(.*?)\$\]', especial_key)[0]
            label = re.findall(r'\[\&(.*?)\&\]', especial_key)[0]

            if isinstance(data_dictionary[especial_key], list):
                for item in data_dictionary[especial_key]:
                    insert_neo4j_from_data_dictionary(
                        item, level+1, label, dict_to_make_node, relationship, father_key, child_key, node_label)
            else:
                insert_neo4j_from_data_dictionary(
                    data_dictionary[especial_key], level+1, label, dict_to_make_node, relationship, father_key, child_key, node_label)


fill_data_dictionary(importDictionary)

arq_name = "./neo4jdb/"+date.today().strftime("%Y%m%dT%H:%M:%S") + \
    "_neo4j_data_dictionary.json"
print("dataDictionary construido e enviado para o arquivo ::::::> "+arq_name)
with open(arq_name, "w") as outfile:
    outfile.write(json.dumps(dataDictionary, indent=4,
                  sort_keys=True, default=str))

insert_neo4j_from_data_dictionary(dataDictionary)

monetdbConn.fechar()
# https://neo4j.com/docs/cypher-manual/current/clauses/create/#create-create-a-full-path
