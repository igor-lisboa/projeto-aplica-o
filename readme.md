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

> docker compose up --build

> docker exec -it projecto_aplicacao_monetdb bash

> monetdb create dataflow_analyzer && monetdb release dataflow_analyzer

> mclient -u monetdb -d dataflow_analyzer
password:<monetdb>

> CREATE USER "dataflow_analyzer" WITH PASSWORD 'dataflow_analyzer' NAME 'Dataflow Analyzer Explorer' SCHEMA "sys";CREATE SCHEMA "dataflow_analyzer" AUTHORIZATION "dataflow_analyzer";ALTER USER "dataflow_analyzer" SET SCHEMA "dataflow_analyzer";CREATE SCHEMA "public" AUTHORIZATION "dataflow_analyzer";ALTER USER "dataflow_analyzer" SET SCHEMA "public";SELECT 'hello world';

> [CTRL + C]

> mclient -u dataflow_analyzer -e -d dataflow_analyzer < ./dados_sciphy.sql > log.txt
password:<dataflow_analyzer>




docker compose up --build -d
docker exec -it projecto_aplicacao_monetdb bash
monetdbd create mydbfarm
cd mydbfarm
monetdbd get all ./
monetdb create sciphy_dados
monetdb release sciphy_dados
cd ../
mclient -u monetdb -d sciphy_dados
password: monetdb
CREATE SCHEMA "public" AUTHORIZATION "monetdb";
ALTER USER "monetdb" SET SCHEMA "public";
\<dados_sciphy.sql