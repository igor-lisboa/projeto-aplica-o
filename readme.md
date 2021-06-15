->problema q começou a tratar agr

-> dado de proveniencia
	-> historico do experimento
		-> momento e oq foi observado
	-> muito experimento simulado no computador
		-> script q executa programas/parte de codigo
			-> pipelines

-> montar framework/biblioteca p ajudar na proveniencia de dados
	-> parametro de entrada/saida

Neo4j
	-> bd grafo

-> pegar banco relacional
	-> estruturar o dado e explorar ele em multiplos sistemas
		-> cassandraDB e monnetDB

-> quais analises nas quais cada um dos bds é forte


=> quais sao os padroes de consulta ?
=> mapear padroes de consulta pra cada consulta em cada BD pra poder aconselhar um BD


=> qual banco performa melhor
	-> testar


=> monnetDB


-> olhar dataset
	-> quais tipos de dados temos la dentro?
	-> quais bancos explorar

***

# por padrao o monetdb vem com user e passoword definidos como monetdb

> docker run -v "$(pwd):/var/www" -d -P --name monetdb monetdb/monetdb:Oct2020-SP3

> docker exec -it monetdb bash

> monetdb create dataflow_analyzer
> monetdb release dataflow_analyzer

> mclient -u monetdb -d dataflow_analyzer
password:<monetdb>

> CREATE USER "dataflow_analyzer" WITH PASSWORD 'dataflow_analyzer' NAME 'Dataflow Analyzer Explorer' SCHEMA "sys";
> CREATE SCHEMA "dataflow_analyzer" AUTHORIZATION "dataflow_analyzer";
> ALTER USER "dataflow_analyzer" SET SCHEMA "dataflow_analyzer";
> CREATE SCHEMA "public" AUTHORIZATION "dataflow_analyzer";
> ALTER USER "dataflow_analyzer" SET SCHEMA "public";
> SELECT 'hello world';

> cd /var/www

> mclient -u dataflow_analyzer -d dataflow_analyzer < ./dados_sciphy.sql > log.txt
password:<dataflow_analyzer>