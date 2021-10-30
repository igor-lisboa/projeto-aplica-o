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
dataflow_execution["consulta"] = "select sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S') as execution_datetime from dataflow_execution de where de.df_id = #$id$#  order by   de.execution_datetime"
dataflow_execution["tipo"] = "primeiro_ou_nulo"
dataflow["execution"] = dataflow_execution
data_transformation = {}
data_transformation["consulta"] = "select dt.id, dt.tag as data_transformation_tag from data_transformation dt"
data_transformation_execution = {}
data_transformation_execution["consulta"] = "select dte.id, dte.dataflow_execution_id, dte.data_transformation_id, sys.str_to_timestamp(dte.execution_datetime, '%Y-%m-%d %H:%M:%S') as current_execution_datetime, LEAD( sys.str_to_timestamp(dte.execution_datetime, '%Y-%m-%d %H:%M:%S') ) over ( order by dte.execution_datetime, dte.id) as next_execution_datetime from data_transformation_execution dte where dte.id = #$id$#"
data_transformation["execution"] = data_transformation_execution
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


def get_dict_by_consulta(consulta_base: str, dict_father: list = None, chave_insrt: str = None, tipo_append: str = "todos"):
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
                nova_consulta)

            if tipo_append == "primeiro_ou_nulo":
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
        return get_result_consulta(consulta_base)


def get_result_consulta(consulta: str):
    retorno = []

    limit = ' LIMIT ' + str(qtdPerPage) + ' '

    pagina = 1

    ultima_pagina = int(monetdbConn.consultar(
        'SELECT ceil(count(*)/' + str(qtdPerPage) + ') FROM (' + consulta + ') x')[0][0])

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
            consulta+limit+offset)

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
