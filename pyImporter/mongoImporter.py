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

importDictionary["dataflow"] = dataflow


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

                mongoConn.insere(
                    chave_pai, tuple_list_to_dictionary(consulta+limit+offset))

                pagina += 1
        else:
            insere_documentos(dictionary[chave], chave)


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
