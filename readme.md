# Framework/biblioteca p ajudar na proveniência de dados
* Estruturar o dado e explorar ele em múltiplos bancos de dados, mapear padrões de consulta e verificar pontos fortes de cada um dos bancos de dados, para aconselhar qual é melhor para cada necessidade de consulta.

 ***

* problema q começou a tratar agr
* dado de proveniencia
	* historico do experimento
		* momento e oq foi observado
	* muito experimento simulado no computador
		* script q executa programas/parte de codigo
			* pipelines
* montar framework/biblioteca p ajudar na proveniencia de dados
	* parametro de entrada/saida
* Neo4j
	* bd grafo
* pegar banco relacional
	* estruturar o dado e explorar ele em multiplos sistemas
		* cassandraDB
		* monnetDB
* quais analises nas quais cada um dos bds é forte
* quais sao os padroes de consulta ?
* mapear padroes de consulta pra cada consulta em cada BD pra poder aconselhar um BD
* qual banco performa melhor
	* testar
* olhar dataset
	* quais tipos de dados temos la dentro?
	* quais bancos explorar

***

### por padrao o monetdb vem com user e passoword definidos como monetdb

***

# Comandos
* docker compose up --build -d
* docker exec -it projeto_aplicacao_monetdb bash
* monetdbd create mydbfarm
* cd mydbfarm
* monetdbd get all ./
* monetdb create sciphy_dados
* monetdb release sciphy_dados
* cd ../
* mclient -u monetdb -d sciphy_dados
* password: monetdb
* CREATE SCHEMA "public" AUTHORIZATION "monetdb";
* ALTER USER "monetdb" SET SCHEMA "public";
* \<dados_sciphy.sql