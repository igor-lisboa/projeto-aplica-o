from data.mongoRepository import MongoRepository
from data.monetRepository import MonetRepository
import re

rodando_no_docker = False
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
dataflow_dataflon = {}
dataflow_dataflon["consulta"] = "select sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S') as execution_datetime from dataflow_execution de where de.df_id = #$id$#  order by   de.execution_datetime"
dataflow["execution"] = dataflow_dataflon
data_transformation = {}
data_transformation["consulta"] = "select dt.id, dt.tag as data_transformation_tag from data_transformation dt"
data_transformation["execution"] = "select dte.id, dte.dataflow_execution_id, dte.data_transformation_id, TO_TIMESTAMP(dte.execution_datetime, 'YYYY-MM-DD HH24:MI:SS') as current_execution_datetime, LEAD( TO_TIMESTAMP(dte.execution_datetime, 'YYYY-MM-DD HH24:MI:SS') ) over ( order by dte.execution_datetime, dte.id) as next_execution_datetime from data_transformation_execution dte where dte.id = #$id$#"
importDictionary["dataflow"] = dataflow
importDictionary["data_transformation"] = data_transformation


def insere_documentos(dictionary: dict, nivel: int = 0):
    chaves = dictionary.keys()

    if 'consulta' in dictionary:
        result = get_dict_by_consulta(dictionary['consulta'])

    for chave in chaves:
        if(nivel == 0):
            mongoConn.insere(chave, insere_documentos(
                dictionary[chave], nivel+1))

        if chave != 'consulta':
            if(type(dictionary[chave]) == str):

                consulta = str(dictionary[chave])
                variaveis = re.findall(r'#$.*$#', consulta)

                for variavel in variaveis:
                    consulta = consulta.replace(
                        '#$'+variavel+'$#', result[variavel])

                result[chave] = get_dict_by_consulta(dictionary[chave])
            else:
                result[chave] = insere_documentos(dictionary[chave], nivel+1)

    return result


def get_dict_by_consulta(consulta: str):
    limit = ' LIMIT ' + str(qtdPerPage) + ' '

    retorno = []

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

        retorno.append(dict_to_insert)

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
