from pymongo import results
from data.mongoRepository import MongoRepository
from data.monetRepository import MonetRepository

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
dataflow["consulta"] = "select   d.id,   d.tag,   sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S') as execution_datetime  from   dataflow d  left join dataflow_execution de on   (d.id = de.df_id)  order by   de.execution_datetime,   d.id"

data_transformation = {}
data_transformation[
    "consulta"] = "select   dte.id,   dte.dataflow_execution_id,   dte.data_transformation_id,   dt.tag as data_transformation_tag,   sys.str_to_timestamp(dte.execution_datetime, '%Y-%m-%d %H:%M:%S') as execution_datetime  from   data_transformation_execution dte  left join data_transformation dt on   (dt.id = dte.data_transformation_id)"

importDictionary["dataflow"] = dataflow
importDictionary["data_transformation"] = data_transformation


def insere_documentos(dictionary: dict, chave_pai: str = ""):
    chaves = dictionary.keys()
    for chave in chaves:
        if(chave == "consulta"):
            consulta = dictionary[chave]

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

                mongoConn.insere(
                    chave_pai, dict_to_insert)

                pagina += 1
        else:
            insere_documentos(dictionary[chave], chave)


def recupera_retornos_pra_colocar_dicionario_a_ser_inserido(dictionary: dict):
    # apenas teste por enquanto
    chaves = dictionary.keys()
    retorno = {}
    for chave in chaves:
        if(chave != "consulta"):
            dict_obj = dictionary[chave]
            monetdbConn.consultar(dict_obj['obj'])

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
