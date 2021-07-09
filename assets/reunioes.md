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

* por padrao o monetdb vem com user e passoword definidos como monetdb

# 06/07
* https://github.com/igor-lisboa/projeto-aplicacao

* por enquanto so usamos monetdb

* dado de proveniencia
	* historico de:
		* script
		* flow
		* (multiplas atividades com entradas e saidas e com dependencias entre elas)
	* tem q registrar a dependencia

## padrao do w3c para dados de proveniencia
* ENTIDADE
	* qq coisa manipulada em um processo
* ATIVIDADES
	* acoes
* AGENTES
	* pessoas ou sistemas q interagem c entidades ou atividades

* MODELO DO PROFESSOR
	* ql dataflow analisado
	* ql transformacao tem
	* ql dependencia 1 transformacao tem c a outra
	* quais sao os arquivos gerados em uma transformacao

## HISTORICO DO Q ESTA ACONTECENDO

* transformacao de dados
	* recebe dado de entrada
	* tem um dado de saida
	* TAREFA
		* realizacao dessa atividade

* qnd executa o programa, vou gerando varias tarefas

1. PRIMEIRO GRAVAMOS A ESTRUTURA

* DUMP Q O GUSTAVO PASSOU É UM EXPERIMENTO DE BIO INFORMATICA



## A IDEIA DO MESTRE DANIEL
* EXPLORAR SISTEMAS DE BANCOS DE DADOS DIFERENTES
* INICIALMENTE FOCAR NO MODELO Q TA LA
	* APLICAR EM OUTROS TIPOS DE BANCOS DE DADOS
		* NEO4J
		* MONGO
* VMS MEDIR
	* TEMPO
	* DIFICULDADE

* TEMOS HJ
* MONET (orientado a coluna)

## QUAIS QUEREMOS AVALIAR? (1A PARTE)
*  mongo (documento)
*  neo4j (GRAFO)
*  redis?dynamoDB?cassandra (chave/valor)
*  postgreSql(relacional)
	* postgresSql (controle de concorrencia é melhor)


* PODEMOS COMPARAR NOSSO MODELO EM VARIOS SISTEMAS
* DPS FAZER NO ProvONE


## TCC 1
* ACOMPANHAMENTO QUE A GNT FAZ
	* ESCREVER PARA ADIANTAR O TRABALHO NA HR DA ESCRITA DO TRABALHO FINAL


* ENTREGAR ESTUDO COMPARATIVO
	* RODAMOS COMBINACOES POSSIVEIS E A CONCLUSAO FOI .....




* SCIPHY (fragmento de um workflow maior)
	* grafico no artigo do BSB


* consumo de disco
* consumo de memoria

* INCIDENCIA DE MODELO EVOLUTIVO


* VARIAS CATEGORIA CONSULTA
* DESEMPENHO


* PRA INICIO PODE SER A CONSULTA Q VERIFICA
	* QL ENTRADA RETORNOU TAL SAIDA?